"""
The user pastes in a list of tasks where each line has the fractional hours as the first word, e.g.:
0.75 plot fixing
0.25 ICLR review plan
0.75 update website and resume with papers
0.5 inbox 0

Then, sum and output the total hours, but cumulatively next the each tas, e.g.:
0.75 plot fixing
1.0 ICLR review plan
1.75 update website and resume with papers
2.25 inbox 0
"""


def main() -> None:
    """Main function."""
    tasks = []
    print(
        "Paste in a list of tasks where each line has the fractional hours as the first word, then press Ctrl+Z (Windows) or Ctrl+D (Unix) to end input:"
    )
    while True:
        try:
            line = input()
        except EOFError:
            break
        line = line.strip()
        if line:
            tasks.append(line)
    if not tasks:
        print("No tasks found.")
        return
    total = 0
    print("\nCumulative hours:")
    for task in tasks:
        try:
            hours, task = task.split(" ", 1)
            total += float(hours)
            print(f"{total} {task}")
        except ValueError:
            print(f"⚠️ Skipping {task} because {hours} is not a number.")

    # Pause before closing.
    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()
