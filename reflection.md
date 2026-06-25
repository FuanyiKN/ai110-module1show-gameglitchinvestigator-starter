# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

1. Hints were innacurate (I expected proper guidance)
2. Enter didn't submit my guess (I didn't expect to have to click after pressing enter)
3. Start new game didn't really start new game (I didn't expect to have to reload the entire tab)

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|   71  |    Go Lower       | Go Higher       | 9                      |
|   25  |    Go Lower       | Go Higher       | 11                     |
|   15  |    Go Higher      | Go Lower        | 28|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I use Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
It suggested that the direction of the hints were reversed, and I verified from my UI tests.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
I didn't run into such an issue.//Editing this

Originally thought we handled bug 1, but there was still a bug that stringifies the target on even attempts, hence producing erroneous feedback. We had to remove that sectin to fix the issue.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
After the test was succesful. 
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
I opened a second terminal since the game was running in another and ran the following code:  python -m pytest test/test_game_logic.py
- Did AI help you design or understand any tests? How?
Yes, it generated the script above to test the logic after we effected the bug fixes. I also reoaded the webpage of the game and tested bug 2 and bug 3's fix.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Stremlit re-runs the whole script from top to bottom every time you interact with the page. The session state acts as a shelf that doesn't get altered by these reruns and remembers things like the secret number and score.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
Understand instructions fully before enaging and document changes
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
Try to do the work without AI before getting AI involved. Well, this is kinda hard cos it says to work with AI. Maybe do the work, and then ask AI for feedback on what I have done
- In one or two sentences, describe how this project changed the way you think about AI generated code.
Not much changed on my end, but it reinforced the position that AI code isn't always reliable and it is important to check before validating.