# GitHub 上传与提交

**当前状态：项目文件已就绪，尚未创建或上传远程仓库。** 上一个工作于2026-10-08检查发现本机已安装 GitHub CLI，但现有登录 token 无效。需要你在自己的浏览器里重新登录；不要在聊天中发送 token。

可上传目录：

`/Users/wangzhe/Documents/Codex/2026-10-08/referenced-chatgpt-conversation-this-is-an-2/outputs/IS507_Midterm_Revised`

## 推荐：终端上传整个目录

在下面目录执行。若仓库已经存在，不重复运行创建命令；先查看 `git remote -v` 和 `gh repo view`。

```sh
cd "/Users/wangzhe/Documents/Codex/2026-10-08/referenced-chatgpt-conversation-this-is-an-2/outputs/IS507_Midterm_Revised"
gh auth login --hostname github.com --git-protocol https --web
gh auth status
gh auth setup-git
git init -b main
git add .
git status --short
git commit -m "Add verified IS507 hotel noncompletion analysis and deliverables"
gh repo create hotel-cancellation-is507 --private --source=. --remote=origin --push
gh repo view --json url --jq .url
```

仓库默认设为 private，避免替你决定公开课程材料。如果老师提供 GitHub 用户名，在仓库 Settings → Collaborators 邀请老师；或按课程允许的方式自行设为 public。公开时确认课程资料允许分享。这里不声称已邀请老师或已完成共享。

若提交时提示缺少Git身份，在此仓库设置你的真实 `user.name` 和你自己的GitHub noreply邮箱，然后重试commit；不要把虚构署名或AI建议的发言角色当作真实贡献。已有本地main初始化不影响再次执行git init；有同名远程仓库时，换名字或连接确认过的仓库，避免覆盖。

## 不使用终端：网页上传

1. 解压 `IS507_Midterm_Revised.zip`。
2. 在 GitHub 的 New repository 页面创建一个仓库；visibility由你决定。
3. 点击 Add file → Upload files，上传解压后 **IS507_Midterm_Revised目录内部** 的文件和子文件夹，不只上传zip。浏览器看不到`.gitignore`时，用Create new file单独创建并复制本地内容。
4. 提交文件后检查README、src、六个notebooks、requirements.txt、deliverables和原始CSV是否存在；不要上传`.venv`、`.cache`或`.git`。
5. 若网页批量上传数量受限，分批上传或使用上面的CLI方法。原始CSV约16MB；无需上传生成的processed数据。
6. 复制真实仓库URL，确认老师可访问，并与PPT/PDF一起提交。

## 上传后核验

从仓库重新clone到新文件夹，按README创建Python环境并运行 `run_all.py`、`run_notebooks.py`、`verify_outputs.py`。验证集Log Loss约0.5517、AUC约0.6584；已有测试Log Loss约0.5968、AUC约0.6644，PDF5页，PPT含11正文+4隐藏备份。新机器的干净依赖安装尚未在本次环境中测试。

官方说明：[gh repo create](https://cli.github.com/manual/gh_repo_create)、[上传文件到仓库](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)。
