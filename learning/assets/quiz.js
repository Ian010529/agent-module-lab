(() => {
  const answeredCorrectly = new Set();

  function refreshGate() {
    document.querySelectorAll('[data-gate]').forEach((gate) => {
      const ids = [...gate.querySelectorAll('[data-quiz-id]')].map((q) => q.dataset.quizId);
      const status = gate.querySelector('[data-gate-status]');
      const passed = ids.length > 0 && ids.every((id) => answeredCorrectly.has(id));
      if (!status) return;
      if (passed) {
        status.textContent = 'Gate passed — tell your teacher “Lesson 0001 gate passed”.';
        status.classList.add('passed');
      } else {
        const done = ids.filter((id) => answeredCorrectly.has(id)).length;
        status.textContent = `Gate: ${done}/${ids.length} correct. Keep going.`;
        status.classList.remove('passed');
      }
    });
  }

  document.querySelectorAll('[data-quiz-id]').forEach((quiz) => {
    const id = quiz.dataset.quizId;
    const correct = quiz.dataset.correct;
    const explanation = quiz.dataset.explanation || '';
    const feedback = quiz.querySelector('[data-feedback]');

    quiz.querySelectorAll('[data-choice]').forEach((button) => {
      button.addEventListener('click', () => {
        quiz.querySelectorAll('[data-choice]').forEach((b) => b.classList.remove('correct', 'wrong'));
        if (button.dataset.choice === correct) {
          button.classList.add('correct');
          answeredCorrectly.add(id);
          if (feedback) feedback.textContent = 'Correct. ' + explanation;
        } else {
          button.classList.add('wrong');
          answeredCorrectly.delete(id);
          if (feedback) feedback.textContent = 'Not yet. Re-read the boundary above, then try again.';
        }
        refreshGate();
      });
    });
  });

  refreshGate();
})();
