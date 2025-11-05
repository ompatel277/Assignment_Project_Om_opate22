"""
Traject Roadmap Generator
Creates semester-by-semester academic and career preparation plans
"""

from typing import List, Dict
from dataclasses import dataclass
from accounts.models import UserProfile, Course
from recommender.engine import RecommendationEngine


@dataclass
class SemesterPlan:
    """Represents a single semester in the roadmap."""
    semester_number: int
    season: str  # 'Fall' or 'Spring'
    year: int
    courses: List[Dict]
    clubs: List[str]
    portfolio_items: List[Dict]
    total_credits: float
    milestones: List[str]


class RoadmapGenerator:
    """
    Generates personalized semester-by-semester roadmaps for students.
    Includes courses, clubs, portfolio items, and career milestones.
    """

    def __init__(self, user_profile: UserProfile):
        self.profile = user_profile
        self.rec_engine = RecommendationEngine(user_profile)

        # Semester settings
        self.target_credits_per_semester = 15  # Typical full-time load
        self.max_semesters = 8  # 4 years = 8 semesters

    def generate_roadmap(self, start_year: int = None, start_season: str = 'Fall') -> List[SemesterPlan]:
        """
        Generate a complete semester-by-semester roadmap.

        Args:
            start_year: Starting year (defaults to current year)
            start_season: 'Fall' or 'Spring'

        Returns:
            List of SemesterPlan objects
        """
        import datetime

        if start_year is None:
            start_year = datetime.datetime.now().year

        roadmap = []
        current_semester_index = self._get_current_semester_index()

        # Generate plans for remaining semesters
        for i in range(current_semester_index, self.max_semesters):
            # Determine season and year
            season = 'Fall' if i % 2 == 0 else 'Spring'
            year = start_year + (i // 2)

            # Generate semester plan
            semester_plan = self._generate_semester(
                semester_number=i + 1,
                season=season,
                year=year
            )

            roadmap.append(semester_plan)

        return roadmap

    def _get_current_semester_index(self) -> int:
        """
        Determine which semester the student is currently in.
        Returns 0-based index (0=Freshman Fall, 1=Freshman Spring, etc.)
        """
        year_map = {
            'FR': 0,
            'SO': 2,
            'JR': 4,
            'SR': 6,
            'GR': 8,
        }
        return year_map.get(self.profile.academic_year, 0)

    def _generate_semester(self, semester_number: int, season: str, year: int) -> SemesterPlan:
        """Generate plan for a single semester."""

        # Get course recommendations
        course_recs = self.rec_engine.get_course_recommendations(
            semester=season, limit=5
        )

        # Select courses up to target credit hours
        selected_courses = []
        total_credits = 0.0

        for rec in course_recs:
            course = rec['course']
            if total_credits + float(course.credits) <= self.target_credits_per_semester:
                selected_courses.append({
                    'course': course,
                    'credits': float(course.credits),
                    'reasoning': rec.get('reasoning', '')
                })
                total_credits += float(course.credits)

            # Stop if we've reached target credits
            if total_credits >= self.target_credits_per_semester - 2:
                break

        # Get club recommendations (consistent across semesters)
        club_recs = self.rec_engine.get_club_recommendations(limit=3)
        club_names = [rec['club'].name for rec in club_recs[:2]]

        # Get portfolio item recommendations (distributed across semesters)
        portfolio_recs = self.rec_engine.get_portfolio_recommendations(limit=8)

        # Assign 1-2 portfolio items per semester based on semester number
        semester_portfolio = self._assign_portfolio_items(
            semester_number, portfolio_recs
        )

        # Generate milestones for this semester
        milestones = self._generate_milestones(semester_number, season)

        return SemesterPlan(
            semester_number=semester_number,
            season=season,
            year=year,
            courses=selected_courses,
            clubs=club_names,
            portfolio_items=semester_portfolio,
            total_credits=total_credits,
            milestones=milestones
        )

    def _assign_portfolio_items(self, semester_number: int, portfolio_recs: List[Dict]) -> List[Dict]:
        """
        Distribute portfolio items across semesters.
        Earlier semesters get easier items, later ones get advanced items.
        """
        # Determine how many items for this semester
        items_per_semester = max(1, len(portfolio_recs) // self.max_semesters)

        # Calculate start and end indices for this semester
        start_idx = (semester_number - 1) * items_per_semester
        end_idx = start_idx + items_per_semester

        # Get items for this semester
        semester_items = portfolio_recs[start_idx:end_idx]

        return [
            {
                'item': rec['item'],
                'reasoning': rec.get('reasoning', ''),
                'estimated_hours': rec['item'].estimated_hours or 0
            }
            for rec in semester_items
        ]

    def _generate_milestones(self, semester_number: int, season: str) -> List[str]:
        """
        Generate career preparation milestones for each semester.
        Milestones become more advanced as semesters progress.
        """
        milestones_by_semester = {
            1: [
                "Attend college orientation and academic advising",
                "Join 1-2 clubs related to your interests",
                "Set up your LinkedIn profile",
                "Explore career options through informational interviews"
            ],
            2: [
                "Build a personal portfolio website or GitHub profile",
                "Attend career fairs to learn about opportunities",
                "Complete a beginner-level online course or certification"
            ],
            3: [
                "Apply for summer internships or research positions",
                "Develop a personal project to showcase your skills",
                "Network with upperclassmen in your field"
            ],
            4: [
                "Complete your first internship or research project",
                "Update your resume and portfolio with summer experience",
                "Attend technical workshops or bootcamps"
            ],
            5: [
                "Take on leadership roles in clubs or organizations",
                "Apply for competitive internships at target companies",
                "Contribute to open-source projects"
            ],
            6: [
                "Complete a significant technical project or capstone",
                "Prepare for technical interviews (LeetCode, etc.)",
                "Attend company recruiting events"
            ],
            7: [
                "Begin full-time job search and interview prep",
                "Network with alumni in your target industry",
                "Prepare your final portfolio and demo reel"
            ],
            8: [
                "Secure full-time job offers or grad school admission",
                "Complete capstone project and graduate",
                "Transition planning and relocation if needed"
            ],
        }

        return milestones_by_semester.get(semester_number, [
            f"Focus on academic excellence and skill development"
        ])

    def generate_summary(self) -> Dict:
        """
        Generate a high-level summary of the roadmap.
        Useful for dashboard display.
        """
        roadmap = self.generate_roadmap()

        total_courses = sum(len(sem.courses) for sem in roadmap)
        total_credits = sum(sem.total_credits for sem in roadmap)
        all_portfolio_items = []
        for sem in roadmap:
            all_portfolio_items.extend(sem.portfolio_items)

        # Get unique clubs across all semesters
        all_clubs = set()
        for sem in roadmap:
            all_clubs.update(sem.clubs)

        return {
            'total_semesters': len(roadmap),
            'total_courses': total_courses,
            'total_credits': total_credits,
            'total_portfolio_items': len(all_portfolio_items),
            'recommended_clubs': list(all_clubs),
            'graduation_year': roadmap[-1].year if roadmap else None,
            'graduation_season': roadmap[-1].season if roadmap else None,
        }


# =====================================================
#  CONVENIENCE FUNCTIONS
# =====================================================

def generate_roadmap_for_user(user_profile: UserProfile) -> List[SemesterPlan]:
    """
    Convenience function to generate a roadmap for a user.
    """
    generator = RoadmapGenerator(user_profile)
    return generator.generate_roadmap()


def get_roadmap_summary(user_profile: UserProfile) -> Dict:
    """
    Get a summary of the roadmap for dashboard display.
    """
    generator = RoadmapGenerator(user_profile)
    return generator.generate_summary()