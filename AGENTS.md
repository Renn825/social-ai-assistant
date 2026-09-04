每次完成改动后,都必须创建一个对应的  git commit ,并将修改记录上传到github,以便后续追踪和回滚.

每次改动后,都必须编写或更新相关测试,并在交付给用户前,确保所有测试和验证全部通过

## 测试与验证（强制）

1. 每次代码改动后，先编写/更新相关测试，再运行完整测试：
   .\.venv\Scripts\python.exe -m pytest -q

2. 测试全部通过后，才允许执行 git commit 和 git push。

3. 若提示缺少依赖，先执行：
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt

4. pre-commit hook 会自动运行完整测试；测试失败会阻止提交。
