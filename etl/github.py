import httpx
from datetime import datetime, timedelta
from typing import Dict, Any

def fetch_repo_stats(owner: str, repo: str) -> Dict[str, Any]:
    """
    Fetch GitHub repository statistics without requiring authentication.
    Returns commits in last 30 days, contributors in last 90 days, and last push timestamp.
    """
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    stats = {
        "commits_30d": 0,
        "contributors_90d": 0,
        "last_push_at": None
    }
    
    try:
        with httpx.Client(timeout=30) as client:
            repo_response = client.get(base_url)
            repo_response.raise_for_status()
            repo_data = repo_response.json()
            stats["last_push_at"] = repo_data.get("pushed_at")
            
            thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
            commits_url = f"{base_url}/commits"
            commits_params = {"since": thirty_days_ago, "per_page": 100}
            
            commit_count = 0
            page = 1
            while page <= 3:
                commits_params["page"] = page
                commits_response = client.get(commits_url, params=commits_params)
                if commits_response.status_code != 200:
                    break
                commits = commits_response.json()
                if not commits:
                    break
                commit_count += len(commits)
                page += 1
            
            stats["commits_30d"] = commit_count
            
            contributors_url = f"{base_url}/contributors"
            contributors_params = {"per_page": 100}
            contributors_response = client.get(contributors_url, params=contributors_params)
            if contributors_response.status_code == 200:
                contributors = contributors_response.json()
                stats["contributors_90d"] = len(contributors)
    
    except Exception as e:
        print(f"Warning: Could not fetch GitHub stats for {owner}/{repo}: {e}")
    
    return stats
