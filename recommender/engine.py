"""
Traject AI Recommendation Engine
Provides skill-based career matching with reasoning
"""

from typing import List, Dict
from django.db.models import Q
from careers.models import Career
from accounts.models import UserProfile, PortfolioItem, Course, Club


class RecommendationEngine:
    """
    AI-powered recommendation engine for matching users with careers,
    courses, clubs, and portfolio items based on skills and interests.
    """

    def __init__(self, user_profile: UserProfile):
        self.profile = user_profile
        self.user_skills = set(self.profile.get_skills_list())
        self.user_interests = set(self.profile.get_interests_list())

    # =====================================================
    #  CAREER RECOMMENDATIONS
    # =====================================================

    def get_career_recommendations(self, limit: int = 5) -> List[Dict]:
        """
        Match user profile with careers based on skill overlap.
        Returns careers with match scores and reasoning.
        """
        all_careers = Career.objects.all()
        recommendations = []

        for career in all_careers:
            match_data = self._calculate_career_match(career)

            if match_data['match_score'] > 0:
                recommendations.append({
                    'career': career,
                    'match_score': match_data['match_score'],
                    'matched_skills': match_data['matched_skills'],
                    'missing_skills': match_data['missing_skills'],
                    'reasoning': match_data['reasoning'],
                })

        # Sort by match score descending
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:limit]

    def _calculate_career_match(self, career: Career) -> Dict:
        """
        IMPROVED: Calculate how well a career matches the user's profile using
        multi-factor scoring: skills, interests, industries, career goals.
        Returns match score (0-100), matched skills, gaps, and reasoning.
        """
        # Get career's required skills
        career_skills = set()
        if isinstance(career.skills, list):
            career_skills = set([s.lower().strip() for s in career.skills])
        elif isinstance(career.skills, str):
            career_skills = set([s.lower().strip() for s in career.skills.split(',') if s.strip()])

        # Get career's industries
        career_industries = set()
        if isinstance(career.industries, list):
            career_industries = set([i.lower().strip() for i in career.industries])

        # Normalize user data
        user_skills_normalized = set([s.lower().strip() for s in self.user_skills])
        user_interests_normalized = set([i.lower().strip() for i in self.user_interests])

        # Get user's preferred industries
        user_industries = set()
        if self.profile.preferred_industries:
            user_industries = set([i.lower().strip() for i in self.profile.preferred_industries.split(',')])

        # Calculate skill overlap (50% weight)
        matched_skills = user_skills_normalized & career_skills
        missing_skills = career_skills - user_skills_normalized

        skill_score = 0
        if len(career_skills) > 0:
            skill_score = (len(matched_skills) / len(career_skills)) * 50

        # Calculate interest alignment (30% weight)
        # Check if user's interests overlap with career title, description, or skills
        interest_score = 0
        career_text = f"{career.title} {career.description}".lower()
        interest_matches = []
        for interest in user_interests_normalized:
            if interest in career_text or interest in career_skills:
                interest_matches.append(interest)
                interest_score += 10
        interest_score = min(interest_score, 30)  # Cap at 30

        # Calculate industry alignment (20% weight)
        industry_score = 0
        if user_industries and career_industries:
            industry_overlap = user_industries & career_industries
            if industry_overlap:
                industry_score = min((len(industry_overlap) / len(career_industries)) * 20, 20)

        # Calculate career goals alignment (bonus, up to 15 points)
        goals_score = 0
        if self.profile.career_goals:
            goals_text = self.profile.career_goals.lower()
            if career.title.lower() in goals_text:
                goals_score = 15  # Direct title match
            elif any(skill in goals_text for skill in career_skills):
                goals_score = 8  # Skills match goals
            elif any(industry in goals_text for industry in career_industries):
                goals_score = 5  # Industry match goals

        # Calculate total match score (capped at 100)
        raw_score = skill_score + interest_score + industry_score + goals_score
        match_score = min(int(raw_score),100) # hard Cap match to at max at 100% career match

        # Boost score if user has work experience related to this career
        if self.profile.work_experience:
            exp_text = self.profile.work_experience.lower()
            if career.title.lower() in exp_text:
                match_score = min(match_score + 10, 100)  # Boost for relevant experience

        # Generate reasoning
        reasoning = self._generate_career_reasoning(
            career, matched_skills, missing_skills, match_score,
            interest_matches, industry_overlap if user_industries and career_industries else []
        )

        return {
            'match_score': min(match_score, 100),
            'matched_skills': list(matched_skills),
            'missing_skills': list(missing_skills),
            'reasoning': reasoning,
        }

    def _generate_career_reasoning(
            self, career: Career, matched: set, missing: set, score: int,
            interest_matches: list = None, industry_overlap: set = None
    ) -> str:
        """IMPROVED: Generate comprehensive explanation for why a career matches."""

        interest_matches = interest_matches or []
        industry_overlap = industry_overlap or set()

        if score >= 80:
            reason = f"**Excellent Match** ({score}%): "

            # Highlight work experience if relevant
            if self.profile.work_experience and career.title.lower() in self.profile.work_experience.lower():
                reason += f"Your work experience directly relates to {career.title}! "

            if matched:
                reason += f"You have strong skills in {', '.join(list(matched)[:3])}. "

            if interest_matches:
                reason += f"Your interests in {', '.join(interest_matches[:2])} align perfectly. "

            if industry_overlap:
                reason += f"You're targeting the right industry. "

            if missing and len(missing) <= 2:
                reason += f"Just polish up on: {', '.join(list(missing))}."
            elif missing:
                reason += f"Consider adding: {', '.join(list(missing)[:2])}."

        elif score >= 60:
            reason = f"**Strong Match** ({score}%): "

            if len(matched) > 0:
                reason += f"You have {len(matched)} out of {len(matched) + len(missing)} key skills. "
                reason += f"Your expertise in {', '.join(list(matched)[:3])} is valuable. "

            if interest_matches:
                reason += f"Your passion for {', '.join(interest_matches[:2])} makes this a great fit. "

            if missing:
                reason += f"Focus on developing: {', '.join(list(missing)[:3])}."

        elif score >= 40:
            reason = f"**Good Match** ({score}%): "

            if matched:
                reason += f"You have relevant experience with {', '.join(list(matched)[:2])}. "

            if interest_matches:
                reason += f"Your interest in {', '.join(interest_matches[:2])} shows strong alignment. "
            elif industry_overlap:
                reason += f"This role fits your target industries. "

            if missing:
                reason += f"Build up skills in: {', '.join(list(missing)[:3])}."

        elif score >= 20:
            reason = f"**Growing Opportunity** ({score}%): "

            if matched:
                reason += f"You have a foundation with {', '.join(list(matched)[:2])}. "

            if interest_matches:
                reason += f"Your interest in {', '.join(interest_matches[:1])} could drive your learning. "

            reason += f"{career.title} requires developing: {', '.join(list(missing)[:3])}. "

            # Suggest pathway
            if self.profile.academic_year in ['FR', 'SO']:
                reason += "You have time to build these skills through coursework and projects."

        else:
            reason = f"**Exploratory Path** ({score}%): {career.title} requires different skills. "

            if interest_matches:
                reason += f"However, your interest in {', '.join(interest_matches[:1])} shows curiosity. "

            reason += "Consider if this aligns with your long-term goals before investing time."

        return reason

    # =====================================================
    #  PORTFOLIO ITEM RECOMMENDATIONS
    # =====================================================

    def get_portfolio_recommendations(self, limit: int = 8) -> List[Dict]:
        """
        Recommend portfolio items (projects, certs) based on:
        1. Current skill level
        2. Career goals
        3. Skill gaps
        """
        recommendations = []
        all_items = PortfolioItem.objects.all()

        # Get user's target careers
        career_recs = self.get_career_recommendations(limit=3)
        target_skills = set()
        for rec in career_recs:
            target_skills.update(rec['missing_skills'])

        for item in all_items:
            item_skills = set([s.lower().strip() for s in item.get_skills_list()])

            # Calculate relevance score
            skill_overlap = len(item_skills & target_skills)
            difficulty_match = self._assess_difficulty_match(item.difficulty_level)

            relevance_score = (skill_overlap * 20) + (difficulty_match * 10)
            relevance_score = min(relevance_score, 100)

            if relevance_score > 0:
                reasoning = self._generate_portfolio_reasoning(item, item_skills, target_skills)
                recommendations.append({
                    'item': item,
                    'relevance_score': relevance_score,
                    'reasoning': reasoning,
                })

        # Sort by relevance
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        return recommendations[:limit]

    def _assess_difficulty_match(self, difficulty: str) -> int:
        """
        Assess if difficulty level matches user's academic year.
        Returns score 0-10.
        """
        year = self.profile.academic_year

        difficulty_map = {
            'FR': {'BEGINNER': 10, 'INTERMEDIATE': 5, 'ADVANCED': 2},
            'SO': {'BEGINNER': 8, 'INTERMEDIATE': 10, 'ADVANCED': 5},
            'JR': {'BEGINNER': 5, 'INTERMEDIATE': 10, 'ADVANCED': 8},
            'SR': {'BEGINNER': 3, 'INTERMEDIATE': 8, 'ADVANCED': 10},
            'GR': {'BEGINNER': 2, 'INTERMEDIATE': 5, 'ADVANCED': 10},
        }

        return difficulty_map.get(year, {}).get(difficulty, 5)

    def _generate_portfolio_reasoning(
            self, item: PortfolioItem, item_skills: set, target_skills: set
    ) -> str:
        """Generate reasoning for portfolio item recommendation."""
        overlap = item_skills & target_skills

        if overlap:
            reason = f"This {item.get_item_type_display().lower()} will help you develop {', '.join(list(overlap)[:2])}, "
            reason += f"which are important for your target careers. "
        else:
            reason = f"This {item.get_item_type_display().lower()} will broaden your skill set. "

        if item.estimated_hours:
            reason += f"Estimated time: {item.estimated_hours} hours. "

        reason += f"Difficulty: {item.get_difficulty_level_display()}."

        return reason

    # =====================================================
    #  COURSE RECOMMENDATIONS
    # =====================================================

    def get_course_recommendations(self, semester: str = 'FALL', limit: int = 6) -> List[Dict]:
        """
        Recommend courses based on:
        1. Major requirements
        2. Career skill gaps
        3. Interests
        """
        recommendations = []

        if not self.profile.major:
            return []

        # Get courses for user's major
        major_courses = Course.objects.filter(major=self.profile.major)

        # Get target skills from career recommendations
        career_recs = self.get_career_recommendations(limit=3)
        target_skills = set()
        for rec in career_recs:
            target_skills.update([s.lower() for s in rec['missing_skills']])

        for course in major_courses:
            # Simple relevance scoring based on course subject/title
            relevance = 0
            course_text = f"{course.subject} {course.title}".lower()

            # Check if course relates to target skills
            for skill in target_skills:
                if skill in course_text:
                    relevance += 10

            # Prioritize based on course level (number)
            try:
                course_level = int(''.join(filter(str.isdigit, course.number))[:1])
                year_level = ['FR', 'SO', 'JR', 'SR', 'GR'].index(self.profile.academic_year) + 1
                if course_level <= year_level + 1:  # Appropriate level
                    relevance += 5
            except:
                pass

            if relevance > 0:
                recommendations.append({
                    'course': course,
                    'relevance_score': relevance,
                    'reasoning': f"Aligns with your major requirements and career interests."
                })

        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        return recommendations[:limit]

    # =====================================================
    #  CLUB RECOMMENDATIONS
    # =====================================================

    def get_club_recommendations(self, limit: int = 5) -> List[Dict]:
        """
        Recommend clubs based on:
        1. User interests
        2. Career goals
        3. College availability
        """
        if not self.profile.college:
            return []

        clubs = Club.objects.filter(college=self.profile.college)
        recommendations = []

        for club in clubs:
            relevance = 0
            club_text = f"{club.name} {club.category} {club.description}".lower()

            # Match with interests
            for interest in self.user_interests:
                if interest.lower() in club_text:
                    relevance += 15

            # Match with skills
            for skill in self.user_skills:
                if skill.lower() in club_text:
                    relevance += 10

            if relevance > 0:
                recommendations.append({
                    'club': club,
                    'relevance_score': relevance,
                    'reasoning': f"This club aligns with your interests and can help you network with like-minded students."
                })

        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        return recommendations[:limit]


# =====================================================
#  CONVENIENCE FUNCTION
# =====================================================

def get_all_recommendations(user_profile: UserProfile) -> Dict:
    """
    Get all recommendations for a user in one call.
    Returns dict with careers, portfolio items, courses, and clubs.
    """
    engine = RecommendationEngine(user_profile)

    return {
        'careers': engine.get_career_recommendations(limit=5),
        'portfolio_items': engine.get_portfolio_recommendations(limit=8),
        'courses': engine.get_course_recommendations(limit=6),
        'clubs': engine.get_club_recommendations(limit=5),
    }