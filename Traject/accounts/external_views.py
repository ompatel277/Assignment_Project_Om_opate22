# accounts/external_views.py
"""
External API Integration: GitHub API
Allows searching for GitHub user profiles for portfolio/career research
"""

import requests
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse


class GitHubUserAPIView(View):
    """
    Class-based view for fetching GitHub user profiles.

    Endpoints:
    - HTML: /accounts/external/github/?username=<username>
    - JSON: /accounts/api/external/github/?username=<username>
    """

    API_BASE_URL = "https://api.github.com/users"

    def get(self, request):
        # Get query parameter
        username = request.GET.get('username', '').strip()
        return_json = request.GET.get('format') == 'json'

        # Build response context
        context = {
            'username': username,
            'user_data': None,
            'repos': [],
            'error': None
        }

        # Only search if username provided
        if username:
            try:
                # Fetch user profile
                user_response = requests.get(
                    f"{self.API_BASE_URL}/{username}",
                    timeout=5,
                    headers={'Accept': 'application/vnd.github.v3+json'}
                )

                # Check for HTTP errors
                user_response.raise_for_status()

                # Parse user data
                user_data = user_response.json()

                # Extract essential fields
                context['user_data'] = {
                    'username': user_data.get('login', 'N/A'),
                    'name': user_data.get('name', 'N/A'),
                    'bio': user_data.get('bio', 'No bio available'),
                    'avatar_url': user_data.get('avatar_url', ''),
                    'html_url': user_data.get('html_url', ''),
                    'public_repos': user_data.get('public_repos', 0),
                    'followers': user_data.get('followers', 0),
                    'following': user_data.get('following', 0),
                    'location': user_data.get('location', 'N/A'),
                    'company': user_data.get('company', 'N/A'),
                    'blog': user_data.get('blog', 'N/A'),
                    'twitter_username': user_data.get('twitter_username', 'N/A'),
                    'created_at': user_data.get('created_at', 'N/A'),
                }

                # Fetch top repositories (limit to 5)
                try:
                    repos_response = requests.get(
                        f"{self.API_BASE_URL}/{username}/repos",
                        params={'sort': 'updated', 'per_page': 5},
                        timeout=5,
                        headers={'Accept': 'application/vnd.github.v3+json'}
                    )
                    repos_response.raise_for_status()
                    repos_data = repos_response.json()

                    context['repos'] = [
                        {
                            'name': repo.get('name', 'N/A'),
                            'description': repo.get('description', 'No description'),
                            'html_url': repo.get('html_url', ''),
                            'language': repo.get('language', 'N/A'),
                            'stars': repo.get('stargazers_count', 0),
                            'forks': repo.get('forks_count', 0),
                        }
                        for repo in repos_data[:5]
                    ]
                except:
                    pass  # Repos are optional

            except requests.exceptions.Timeout:
                context['error'] = "Request timed out. Please try again."
            except requests.exceptions.ConnectionError:
                context['error'] = "Could not connect to GitHub API."
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    context['error'] = f"GitHub user '{username}' not found."
                elif e.response.status_code == 403:
                    context['error'] = "GitHub API rate limit exceeded. Try again later."
                else:
                    context['error'] = f"HTTP Error: {e.response.status_code}"
            except requests.exceptions.RequestException as e:
                context['error'] = f"Error fetching data: {str(e)}"
            except ValueError:
                context['error'] = "Invalid response from GitHub API."

        # Return JSON or HTML
        if return_json:
            return JsonResponse({
                'ok': context['error'] is None,
                'username': context['username'],
                'user_data': context['user_data'],
                'repos': context['repos'],
                'error': context['error']
            }, status=200 if context['error'] is None else 502)

        return render(request, 'accounts/external_github_search.html', context)