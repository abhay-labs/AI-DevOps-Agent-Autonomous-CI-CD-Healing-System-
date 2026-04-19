import git

def format_branch(team, leader):
    team = team.upper().replace(" ", "_")
    leader = leader.upper().replace(" ", "_")

    return f"{team}_{leader}_AI_Fix"

def commit_and_push(repo_path, fixes, team, leader):

    repo = git.Repo(repo_path)

    branch = format_branch(team, leader)

    new_branch = repo.create_head(branch)
    repo.head.reference = new_branch

    repo.git.add(A=True)
    repo.index.commit("[AI-AGENT] Automated Fix Commit")

    # push disabled for safety (enable later)
    # repo.git.push("--set-upstream", "origin", branch)

    return branch
