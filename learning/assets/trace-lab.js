(() => {
  'use strict';
  const quizzes = [...document.querySelectorAll('[data-quiz-id]')];
  const correct = new Set();
  const summary = document.querySelector('[data-check-summary]');
  const refresh = () => {
    if (summary) summary.textContent = `自检：${correct.size}/${quizzes.length} 题答对。选择题只提供反馈；Final Gate 仍需提交自己的解释并讲评。`;
  };
  quizzes.forEach((quiz) => {
    const buttons = [...quiz.querySelectorAll('[data-choice]')];
    buttons.forEach((button) => button.addEventListener('click', () => {
      const isCorrect = button.dataset.choice === quiz.dataset.correct;
      buttons.forEach((item) => {
        item.classList.remove('correct', 'wrong');
        item.setAttribute('aria-pressed', String(item === button));
      });
      button.classList.add(isCorrect ? 'correct' : 'wrong');
      if (isCorrect) correct.add(quiz.dataset.quizId); else correct.delete(quiz.dataset.quizId);
      quiz.querySelector('[data-feedback]').textContent = `${isCorrect ? '答对了。' : '再想一步。'}${button.dataset.rationale}`;
      refresh();
    }));
  });
  refresh();

  const paths = {
    accept: {
      count: 1,
      path: 'interrupt → accept → invoke(original_args) → tool message → llm_call',
      detail: '接受原参数后执行 Tool，再把 observation 连同原 tool_call_id 回给模型。',
      content: '原 content：Could you confirm the quote currency?'
    },
    edit: {
      count: 1,
      path: 'interrupt → edit → update AIMessage → invoke(edited_args) → tool message → llm_call',
      detail: '编辑是修改参数并执行，不是只保存文字。源码保留同一个 tool_call_id，并让后续消息反映编辑后的参数。',
      content: '编辑后 content：Could you confirm which currency your quote uses?'
    },
    ignore: {
      count: 0,
      path: 'interrupt → ignore → tool message (ignored) → END',
      detail: 'write_email 不执行。应用记录忽略结果，并结束这条 workflow。',
      content: '原 content 没有交给 Tool。'
    },
    response: {
      count: 0,
      path: 'interrupt → response → tool message (feedback) → llm_call',
      detail: '反馈先回给模型。本次不执行 write_email；如果模型随后提出新的 write_email，请求仍会再次走审查边界。',
      content: '人类反馈示例：请只询问币种，别承诺合作。'
    }
  };
  const trace = document.querySelector('[data-trace-output]');
  const actions = [...document.querySelectorAll('[data-trace-action]')];
  actions.forEach((button) => button.addEventListener('click', () => {
    const state = paths[button.dataset.traceAction];
    actions.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    trace.querySelector('[data-trace-path]').textContent = state.path;
    trace.querySelector('[data-trace-count]').textContent = `本次路径的 tool.invoke 次数：${state.count}`;
    trace.querySelector('[data-trace-detail]').textContent = state.detail;
    trace.querySelector('[data-trace-content]').textContent = state.content;
  }));
  document.querySelector('[data-trace-reset]')?.addEventListener('click', () => {
    actions.forEach((item) => item.setAttribute('aria-pressed', 'false'));
    trace.querySelector('[data-trace-path]').textContent = 'AIMessage.tool_calls → interrupt → 等待人类决定';
    trace.querySelector('[data-trace-count]').textContent = '本次路径的 tool.invoke 次数：0';
    trace.querySelector('[data-trace-detail]').textContent = '先预测哪两个选择会执行 Tool，再点选验证。';
    trace.querySelector('[data-trace-content]').textContent = '待审 content：Could you confirm the quote currency?';
  });

  document.querySelector('[data-export-answers]')?.addEventListener('click', () => {
    const answers = [...document.querySelectorAll('[data-answer]')];
    const body = ['Lesson 0003 — Final Gate 回答', '状态：待讲评，不代表 gate 已通过。', '',
      ...answers.map((field, i) => `${i + 1}. ${document.querySelector(`label[for="${field.id}"]`).textContent.trim()}\n${field.value.trim() || '（未作答）'}\n`)
    ].join('\n');
    const url = URL.createObjectURL(new Blob([body], {type: 'text/plain;charset=utf-8'}));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'lesson-0003-my-answers.txt';
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    document.querySelector('[data-export-status]').textContent = '回答文件已生成。请把自己的回答发回对话进行讲评；页面不会自动提交。';
  });
})();
