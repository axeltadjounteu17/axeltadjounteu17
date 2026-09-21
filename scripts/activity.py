#!/usr/bin/env python3
"""Génère le tableau de bord d'activité (graphique de contributions, langages, répartition)
à partir de l'API GraphQL de GitHub, aux couleurs du portfolio.

    GH_TOKEN=ghp_xxx python3 scripts/activity.py --user ton-pseudo
    python3 scripts/activity.py --demo /tmp/apercu     # aperçu avec de fausses données, n'écrit pas dans assets/

En CI, .github/workflows/activity.yml l'exécute chaque jour.
Le jeton par défaut (GITHUB_TOKEN) ne voit que les contributions publiques. Pour inclure les
contributions privées, crée un jeton personnel (scope read:user) et enregistre-le en secret PROFILE_TOKEN.
"""
import argparse
import datetime as dt
import json
import os
import random
import urllib.request
from pathlib import Path

import build as B

QUERY = """query($login:String!){user(login:$login){
  contributionsCollection{
    totalCommitContributions totalIssueContributions totalPullRequestContributions totalPullRequestReviewContributions
    contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel weekday}}}}
  repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){
    nodes{languages(first:6,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
}}"""
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fetch(user, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"Bearer {token}", "User-Agent": "profile-activity", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload or not payload.get("data", {}).get("user"):
        raise SystemExit(f"Erreur API GitHub : {payload.get('errors') or 'utilisateur introuvable'}")
    return payload["data"]["user"]


def streaks(days):
    counts = [d["count"] for d in days]
    longest = cur = 0
    for c in counts:
        cur = cur + 1 if c else 0
        longest = max(longest, cur)
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:  # la journée en cours ne casse pas la série
        i -= 1
    current = 0
    while i >= 0 and counts[i]:
        current += 1
        i -= 1
    return current, longest


def shape(user):
    cc = user["contributionsCollection"]
    weeks, flat = [], []
    for w in cc["contributionCalendar"]["weeks"]:
        week = [{"date": d["date"], "count": d["contributionCount"], "level": LEVELS[d["contributionLevel"]], "weekday": d["weekday"]}
                for d in w["contributionDays"]]
        weeks.append(week)
        flat += week
    size, color = {}, {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            size[e["node"]["name"]] = size.get(e["node"]["name"], 0) + e["size"]
            color[e["node"]["name"]] = e["node"]["color"] or "#2563EB"
    total = sum(size.values()) or 1
    langs = [(n, color[n], v * 100 / total) for n, v in sorted(size.items(), key=lambda kv: -kv[1])[:6]]
    current, longest = streaks(flat)
    return {"total": cc["contributionCalendar"]["totalContributions"], "commits": cc["totalCommitContributions"],
            "prs": cc["totalPullRequestContributions"], "issues": cc["totalIssueContributions"],
            "reviews": cc["totalPullRequestReviewContributions"], "streak": current, "longest": longest,
            "weeks": weeks, "langs": langs, "updated": dt.date.today().isoformat()}


def demo():
    rnd, start, weeks = random.Random(7), dt.date.today() - dt.timedelta(days=370), []
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)
    d = start
    for _ in range(53):
        wk = []
        for wd in range(7):
            n = 0 if rnd.random() < .55 else rnd.randint(1, 14)
            wk.append({"date": d.isoformat(), "count": n, "level": 0 if n == 0 else min(4, 1 + n // 4), "weekday": wd})
            d += dt.timedelta(days=1)
        weeks.append(wk)
    return {"total": 412, "commits": 331, "prs": 38, "issues": 21, "reviews": 22, "streak": 6, "longest": 19, "weeks": weeks,
            "langs": [("TypeScript", "#3178c6", 46.2), ("Python", "#3572A5", 21.5), ("HCL", "#844FBA", 14.8), ("Dart", "#00B4AB", 9.9), ("Shell", "#89e051", 7.6)],
            "updated": dt.date.today().isoformat()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user")
    ap.add_argument("--demo", metavar="DOSSIER", help="écrit un aperçu avec de fausses données dans ce dossier")
    a = ap.parse_args()
    if a.demo:
        data, out = demo(), Path(a.demo)
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not (a.user and token):
            raise SystemExit("Il faut --user et la variable d'environnement GH_TOKEN")
        data, out = shape(fetch(a.user, token)), B.REPO / "assets"
    for theme, th in B.THEMES.items():
        for lang in B.LANGS:
            B.write(out / theme / f"activity.{lang}.svg", B.activity(th, lang, data))
    print("activité écrite dans", out)


if __name__ == "__main__":
    main()
