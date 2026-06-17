# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.
## summary: Add regression tests for all game logic and update reflection

- Expand tests/test_game_logic.py from 5 to 19 cases covering
  check_guess, get_range_for_difficulty, parse_guess, and update_score
- Add a regression test for every fixed bug: reversed hints, swapped
  Normal/Hard ranges, and scoring (wrong guesses never add points,
  first-guess win awards 90, 10-point floor)
- Add parse_guess coverage: integers, decimals, empty, None, non-numbers
- Fill in reflection.md sections 2 and 3 (AI collaboration + testing)

## 1. What was broken when you started?
## The game would say lower even after hitting the min value (1) or say higher even after guessing atleast the max value (100). The game was supposed to give hints that indicated to guess within the range or to not go beyond the limits already given.
## The New Game button does not work and still says start a new game so new game does not start. The button was supposed to start a new game.
## When you change difficulty the new range is not applied to the new game.
## Normal and hard difficulty range seem switched
- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 60    | Go Lower          | Go Higher       | none                   |
| 30    | Go Higher         | Go Lower        | none                   |
| Easy  | Range 1 to 20     | Range 1 to 100  | none                   |
| Normal| Range 1 to 50     | Range 1 to 100  | none                   |


---

## 2. How did you use AI as a teammate?
## I used AI by inputting the bugs I found into Claude so that Claude can explain which lines are causing the problems. 
## They pointed out the if statements that return Go Higher or Go Lower have the conditions flipped, which is more of a logical error than a compliling error.
## AI helped move lines to code to different files and helped reccomend solutions and also understand synthax I don't know.

I used Claude (Claude Code, in agent mode inside VS Code) as my AI teammate.

**Correct suggestion:** When I reported that the game sometimes told me "Go Higher" when I was already too high, the AI pointed to `check_guess` and explained the hint branches were flipped, and it also found a hidden cause in `app.py` where the secret was being turned into a string (`secret = str(...)`) on even-numbered guesses, so a number was being compared to text. This was correct. I verified it by playing the game (guessing too high and too low on back-to-back turns and watching the hints), and by adding pytest tests `test_too_high_tells_player_to_go_lower` and `test_too_low_tells_player_to_go_higher`, which passed.

**Incorrect / misleading suggestion:** When the AI refactored `check_guess` into `logic_utils.py`, it removed the old `try/except` safety net, which would have *crashed* the app on every even guess because `app.py` was still passing a string secret. So that "clean" refactor was misleading on its own — it was only safe after I also removed the `str(...)` line in `app.py`. I caught it because the AI warned me the app would crash, and I verified by running `streamlit run app.py` and making a second guess (no error anymore). The AI also left a duplicate `import` block at one point that I noticed while reviewing the diff.

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed by checking it two ways: running the live game with `streamlit run app.py` and reproducing the original broken behavior, and running the automated tests with `pytest` from the project root. For the hint bug, I ran `pytest` and all 5 tests passed (the 3 starter tests plus my 2 new ones in `tests/test_game_logic.py`). The starter tests actually had to be fixed first because they compared `result == "Win"`, but `check_guess` returns a tuple `(outcome, message)` — so I unpacked it as `outcome, message = check_guess(...)`, which showed me the function's real return shape. I also found a bug that tests didn't catch: while play-testing I got "Out of attempts!" while the screen still showed one attempt left, and the AI traced it to the `attempts` counter starting at 1 instead of 0. AI helped me design the tests by suggesting concrete cases (guess 60 vs secret 50 should be "Too High" and the message should contain "LOWER"), which made the tests target the exact bug instead of just checking the outcome label.

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state? Reruns are when you interact with a website or feature, it reruns the entire code to actually run the lines dedicated for that specific interaction. Session state is needed because reruns will reset variables unneccesarily so the values are reset to original values when it's not intended to, the session state will preserve the memory so variables like attempts isn't reset everytime a player guesses.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits
## I plan to use AI to assist in understanding why my code doesn't work, not just fixing it completely for me as I want to understand the functions of the code and how everything is connected and results in a certain type of issue being caused and why it can't easily be fixed. This project showed me AI can be a tool to help us understand our code better instead of completely erasing human creativity and learning in the process. My prompting strategy was describing the issue and how it could be fixed or trying to guide through the process to troubleshoot.
- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
