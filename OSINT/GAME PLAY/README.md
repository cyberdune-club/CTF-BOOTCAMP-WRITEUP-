Perfect — here’s a clean, professional **README.md** for your OSINT challenge **“GAME PLAY”** (Points: 498), formatted in the same style as your CTF GitHub repo:

---

```markdown
# 🎮 GAME PLAY

**Category:** OSINT  
**Points:** 498  
**Solves:** 3  
**Likes:** 2  

---

## 📜 Challenge Description

An old post from a well-known **game developer** reveals that he was once **impressed by a speedrun** of one of his games.  
The goal is to track down the **specific game**, the **website** where the speedrun was hosted, the **rating** of that video, and finally, the **developer’s email address**.

Find all the required details and format your answer as a single flag.

---

## 🧩 Flag Format

```

Securinets{game_website_rating_email}

```

---

## 💡 Hints

- “Way back in the day” refers to the early **2000s** — focus on platforms active in that era.  
- **Edmund McMillen** is a key name — investigate his posts, developer accounts, and archived sites.  
- Use the **Wayback Machine** to access defunct or unreachable websites.  

---

## 🧠 Objective

Use open-source intelligence to piece together:
1. The **game** mentioned.  
2. The **platform** where the speedrun was posted.  
3. The **rating** given to the video.  
4. The **email address** of the developer.

---

## 🧾 Write-Up

In this write-up, I’ll guide you through my step-by-step process, the tools I used, and the crucial pivots that eventually led me to the flag. I’ve made sure to keep everything clear and beginner-friendly so other players can easily follow along.

---

### 🧩 Step 1 — Understanding the Clues

From the challenge description, we extract several hints:
- “Way back in the day” → an **old website** (2000s era)
- “Edmund McMillen” → a **game developer**
- “Impressed by a speedrun” → related to a **speedrun video**
- “Rating” → a **video platform** that allows comments and ratings (5–10 scale)

---

### 🔎 Step 2 — Initial Research

I began by searching for platforms that hosted speedruns in the 2000s.  
One popular site at that time was **GameTrailers.com** — a major hub for video uploads and community ratings.

While exploring **Edmund McMillen’s** old posts, I discovered that he indeed had an account on this platform.

---

### 🧠 Step 3 — Finding the Post

Searching for the keyword **“speed”** in his post section revealed a message about being impressed by a **speedrun** of one of his games — **Gish**.  
This confirmed two elements:
- **Game:** Gish  
- **Site:** GameTrailers.com  

---

### 🕰️ Step 4 — Wayback Machine

The link in his post (“here”) led to a dead page.  
Using the **Wayback Machine**, I navigated to archived versions of GameTrailers from **August 2005** (the same date as his post).

That snapshot revealed a **rating** of **6.7** for the video.

---

### 💌 Step 5 — Finding the Email

The archived comments and metadata did not contain any email information.  
So I returned to **Newgrounds.com**, another site where Edmund McMillen published games, and manually searched for `@` across multiple pages.

Eventually, I found the developer’s contact:
```

[souldescen@aol.com](mailto:souldescen@aol.com)

```

---

### 🏁 Final Flag

```

CYBERDUNE{[gish_gametrailers.com_6.7_souldescen@aol.com](mailto:gish_gametrailers.com_6.7_souldescen@aol.com)}

```

---

**Author:** _CyberDune Team_  
**Category:** OSINT / Historical Investigation  
```

---

