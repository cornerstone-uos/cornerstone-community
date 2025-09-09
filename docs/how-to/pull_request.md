# Submitting a pull request

We are going to follow up with the files used the previous section, but nonetheless the steps are similar for a basic submission.

## Upload the files and push to the fork

To upload the files through the browser in GitHub, go to the relevant folder (`SiN_300nm/components` in this case) and select `Upload files` from the `Add files` menu. As GitHub Web UI only allows uploads to a single folder at a time, you will need to upload new cross-sections (if they exist) over multiple commits - if you are using Git in your computer, then these can be done in a single commit.

<img src="../_static/Upload_1.png" class="align-center" width="900" alt="image" />

After the upload, you can specify the commit details for your benefit. Subsequently, you can commit directly to your fork's `main`. **Note**: The second option will invoke a pull request *within* your fork. You are free to do so, but it is not necessary for our purpose. If you are concerned with tidiness of your `main`, you should create a new branch from the fork `main` and commit directly to that branch.

<img src="../_static/Upload_2.png" class="align-center" width="900" alt="image" />

Your fork will look similar to the one below following the commit and push:

<img src="../_static/Push_to_fork.png" class="align-center" width="900" alt="image" />

## Create a pull request to the Community Repository

After you uploaded all the new/modified files and would like to make a submission, select `Open pull request` from `Contribute`. It is a good idea to sync to the latest version of the Community Repository from `Sync fork` and change the referred commit hash keys in the derived/modified components.

<img src="../_static/PullRequest_1.png" class="align-center" width="900" alt="image" />

This will create a pull request template with a Markdown-format commit message for the contributor to modify and fill (see the template [here](https://github.com/cornerstone-uos/cornerstone-community/blob/main/.github/pull_request_template.md))

You can preview the commit message (see below) from the `Preview` button above the edit box: To mark a checkbox, swap `[ ]` with `[x]` (alternatively you can directly mark them after submitting the PR).

<img src="../_static/PullRequest_2.png" class="align-center" width="600" alt="image" />


**Update: No the users can select different `Basic`, `Advanced` or `Documentation` submission templates. Please use the links in Preview to jump to the desired template.**

Click `Create pull request` to start the review process by the CORNERSTONE PDK Team.