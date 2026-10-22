# Contributing

Thanks for helping! The easiest ways to contribute are opening an issue (an unclear explanation, a wrong check, a typo) or sending a pull request with a fix.

## Adding or changing an exercise

Each exercise should have:

1. A **title** and a **kind**: `Predict`, `Fix`, `Arrange`, `Make`, `Challenge` or `Your turn`.
2. A **quick review** of the concept (a few lines, with a small example if useful).
3. A clear **task** that says which names to create or which function to write.
4. A **check** cell. Prefer several cases, including edge cases (empty input, zero, boundaries).
5. A **solution** in the matching notebook under `solutions/`.

Guidelines:

- Use only ideas taught in the current or earlier lessons.
- Keep it short. Put harder ideas in `Challenge` exercises.
- Check messages should help the learner think, not give the answer.

## Testing

The solution notebooks must run without errors:

```bash
pip install -r requirements-dev.txt
pytest --nbmake solutions/
```

The same command runs on every push through GitHub Actions. Also make sure the notebook in `level-1-basics/` fails its checks with the starter code (an exercise whose check already passes before the learner writes anything is a bug).
