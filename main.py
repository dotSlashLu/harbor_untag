# coding=utf8
import api

KEEP = 5
DELETED_TIME = "0001-01-01T00:00:00Z"


def exp_proj(proj):
    repos = api.repos(proj["project_id"])
    expired = [
        (repo["name"],
            # 按创建时间倒排
            sorted(
                # 过滤已经删掉的
                filter(
                    lambda x: x["created"] != DELETED_TIME,
                    api.tag(repo)
                ),
                key=lambda i: i["created"],
                reverse=True
            )[KEEP:])
        for repo in repos
        if repo["tags_count"] > KEEP
    ]

    for exp in expired:
        repo = exp[0]
        repo_tags = exp[1]
        [api.delete(repo, tag["name"]) for tag in repo_tags]


if __name__ == "__main__":
    api.login()
    for proj in api.projs():
        exp_proj(proj)
