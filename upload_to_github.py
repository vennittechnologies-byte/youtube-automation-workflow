#!/usr/bin/env python3
"""
Automated GitHub Upload Script
Uploads the YouTube Automation Workflow to vennittechnologies-byte repository
"""

import os
import sys
import json
import base64
import subprocess
from pathlib import Path
from typing import Dict, List

try:
    import requests
except ImportError:
    print("❌ Error: requests library not installed")
    print("Install with: pip install requests")
    sys.exit(1)


class GitHubUploader:
    """Automate GitHub repository creation and file upload"""
    
    def __init__(self, token: str, username: str, repo_name: str):
        self.token = token
        self.username = username
        self.repo_name = repo_name
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_repository(self, description: str, private: bool = False) -> bool:
        """Create a new GitHub repository"""
        
        url = f"{self.api_base}/user/repos"
        
        data = {
            "name": self.repo_name,
            "description": description,
            "private": private,
            "auto_init": False
        }
        
        print(f"🔨 Creating repository: {self.username}/{self.repo_name}")
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            print(f"✅ Repository created successfully!")
            return True
        elif response.status_code == 422:
            print(f"⚠️  Repository already exists, will update files")
            return True
        else:
            print(f"❌ Failed to create repository: {response.status_code}")
            print(f"   Response: {response.json()}")
            return False
    
    def get_file_content(self, filepath: Path) -> str:
        """Read and base64 encode file content"""
        
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            return base64.b64encode(content).decode('utf-8')
        except Exception as e:
            print(f"❌ Error reading {filepath}: {e}")
            return None
    
    def upload_file(self, filepath: Path, github_path: str) -> bool:
        """Upload a single file to GitHub"""
        
        url = f"{self.api_base}/repos/{self.username}/{self.repo_name}/contents/{github_path}"
        
        # Get file content
        content = self.get_file_content(filepath)
        if content is None:
            return False
        
        # Check if file already exists
        response = requests.get(url, headers=self.headers)
        
        data = {
            "message": f"Add {github_path}",
            "content": content
        }
        
        # If file exists, need to provide sha for update
        if response.status_code == 200:
            existing = response.json()
            data["sha"] = existing["sha"]
            data["message"] = f"Update {github_path}"
        
        response = requests.put(url, headers=self.headers, json=data)
        
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"❌ Failed to upload {github_path}: {response.status_code}")
            return False
    
    def should_ignore(self, path: Path, gitignore_patterns: List[str]) -> bool:
        """Check if file should be ignored based on .gitignore"""
        
        path_str = str(path)
        
        # Always ignore these
        always_ignore = ['.git', '__pycache__', '.pyc', '.DS_Store', '.env']
        for pattern in always_ignore:
            if pattern in path_str:
                return True
        
        # Check gitignore patterns
        for pattern in gitignore_patterns:
            if pattern.strip() and not pattern.startswith('#'):
                if pattern in path_str or path_str.endswith(pattern):
                    return True
        
        return False
    
    def upload_directory(self, source_dir: Path, prefix: str = "") -> Dict[str, int]:
        """Upload entire directory structure"""
        
        # Read .gitignore
        gitignore_file = source_dir / '.gitignore'
        gitignore_patterns = []
        if gitignore_file.exists():
            with open(gitignore_file, 'r') as f:
                gitignore_patterns = f.readlines()
        
        stats = {"success": 0, "failed": 0, "skipped": 0}
        
        # Walk through directory
        for root, dirs, files in os.walk(source_dir):
            root_path = Path(root)
            
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self.should_ignore(root_path / d, gitignore_patterns)]
            
            for filename in files:
                filepath = root_path / filename
                
                # Skip ignored files
                if self.should_ignore(filepath, gitignore_patterns):
                    stats["skipped"] += 1
                    continue
                
                # Calculate relative path for GitHub
                relative_path = filepath.relative_to(source_dir)
                github_path = str(relative_path).replace('\\', '/')
                
                if prefix:
                    github_path = f"{prefix}/{github_path}"
                
                print(f"📤 Uploading: {github_path}")
                
                if self.upload_file(filepath, github_path):
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
        
        return stats


def main():
    """Main execution"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║    🚀 Automated GitHub Upload                                 ║")
    print("║    📦 YouTube Automation Workflow                             ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    # Configuration
    USERNAME = "vennittechnologies-byte"
    REPO_NAME = "youtube-automation-workflow"
    DESCRIPTION = "End-to-End YouTube Video Upload Workflow - Automated video creation with AI, TTS, and stock footage"
    
    # Get GitHub token
    print("🔑 GitHub Personal Access Token Required")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("To create a token:")
    print("  1. Go to: https://github.com/settings/tokens")
    print("  2. Click 'Generate new token (classic)'")
    print("  3. Select scopes: repo (all), workflow")
    print("  4. Click 'Generate token'")
    print("  5. Copy the token (you won't see it again!)")
    print()
    
    token = input("Enter your GitHub Personal Access Token: ").strip()
    
    if not token:
        print("❌ Token is required!")
        sys.exit(1)
    
    print()
    print(f"📋 Configuration:")
    print(f"   Username: {USERNAME}")
    print(f"   Repository: {REPO_NAME}")
    print()
    
    # Confirm
    proceed = input("Proceed with upload? (Y/n): ").strip().lower()
    if proceed == 'n':
        print("Upload cancelled.")
        sys.exit(0)
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    # Initialize uploader
    uploader = GitHubUploader(token, USERNAME, REPO_NAME)
    
    # Create repository
    if not uploader.create_repository(DESCRIPTION, private=False):
        print("❌ Failed to create/access repository")
        sys.exit(1)
    
    print()
    
    # Get project directory
    project_dir = Path(__file__).parent.resolve()
    print(f"📂 Project directory: {project_dir}")
    print()
    
    # Upload files
    print("📤 Uploading files...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    stats = uploader.upload_directory(project_dir)
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("✅ Upload Complete!")
    print()
    print(f"📊 Statistics:")
    print(f"   ✅ Uploaded: {stats['success']} files")
    print(f"   ❌ Failed: {stats['failed']} files")
    print(f"   ⏭️  Skipped: {stats['skipped']} files")
    print()
    print(f"🔗 Repository URL:")
    print(f"   https://github.com/{USERNAME}/{REPO_NAME}")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == "__main__":
    main()
