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
        Calculate how well a career matches the user's profile.
        Returns match score (0-100), matched skills, gaps, and reasoning.
        """
        # Get career's required skills
        career_skills = set()
        if isinstance(career.skills, list):
            career_skills = set([s.lower().strip() for s in career.skills])
        elif isinstance(career.skills, str):
            career_skills = set([s.lower().strip() for s in career.skills.split(',') if s.strip()])

        # Normalize user skills for comparison
        user_skills_normalized = set([s.lower().strip() for s in self.user_skills])

        # Calculate skill overlap
        matched_skills = user_skills_normalized & career_skills
        missing_skills = career_skills - user_skills_normalized

        # Calculate match score
        if len(career_skills) == 0:
            match_score = 0
        else:
            match_score = int((len(matched_skills) / len(career_skills)) * 100)

        # Generate reasoning
        reasoning = self._generate_career_reasoning(
            career, matched_skills, missing_skills, match_score
        )

        return {
            'match_score': match_score,
            'matched_skills': list(matched_skills),
            'missing_skills': list(missing_skills),
            'reasoning': reasoning,
        }

    def _generate_career_reasoning(
            self, career: Career, matched: set, missing: set, score: int
    ) -> str:
        """Generate human-readable explanation for why a career matches."""

        if score >= 70:
            reason = f"✨ **Strong Match** ({score}%): You already have {len(matched)} out of {len(matched) + len(missing)} key skills for {career.title}. "
            if matched:
                reason += f"Your skills in {', '.join(list(matched)[:3])} align well with this role. "
            if missing:
                reason += f"Consider developing: {', '.join(list(missing)[:3])}."
        elif score >= 40:
            reason = f"🎯 **Good Match** ({score}%): You have {len(matched)} relevant skills for {career.title}. "
            if matched:
                reason += f"Your experience in {', '.join(list(matched)[:2])} is valuable. "
            if missing:
                reason += f"To strengthen your fit, focus on: {', '.join(list(missing)[:3])}."
        elif score > 0:
            reason = f"💡 **Growing Opportunity** ({score}%): {career.title} could be a future path. "
            if matched:
                reason += f"You have some foundation with {', '.join(list(matched)[:2])}. "
            if missing:
                reason += f"Key areas to develop: {', '.join(list(missing)[:3])}."
        else:
            reason = f"📚 **Exploratory Path**: {career.title} requires different skills. Consider if this aligns with your long-term interests."

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