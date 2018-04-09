## How to make `message` modules

0.  The `message` modules are the core of tekin's services. Each module (comm) reacts to one or a few types of messages posted to where tekin could see with python's regex module.

1.  The module needs the two base components everything other modules need, i.e., `process(request)` method and `post(request, response)` method. The module also needs an extra attribute called `comm_re`(command_reg_ex). This component is a compiled regex pattern; so in your module, you should state something like:
    ```{python}
    import re
    comm_re = re.compile('your regex here', flags=re.IGNORECASE) 
    #remove the flag if your command is sensitive to cases, of course
    ```

    If in your regex, you need to process `@tekin`, you can use `from tekinbot.utils.config import tekin_id`, then format it into your regex string.

2.  For each message Tekin sees, Tekin tries to match it with all the `comm_re`s from all the message comms it has; if one or more command matches, tekin calls the `process` methods with the request object sent from slack. For what the request jsons look like for messages, see [here](https://api.slack.com/events/message.channels) for an example. Note that this `event` dictionary is wrapped within the [`events` objects](https://api.slack.com/events-api#receiving_events).

3.  Your `process(request)` method should return a string containing what you would like Tekin to say in response to the message.

4.  You should also implement the `post(request, response)` method. Normally, most of the posting are similar, so we DRYed them up in [`tekinbot.utils.post`](https://github.com/nanflasted/TekinBot/blob/documentation-branch/tekinbot/utils/post.py). If you don't see your posting methods there, consider whether the contents you post and/or the actions you'd like tekin to perform right before/after posting could be reused or done in the `process()` method. If so, implement your extra actions at their rightful places; otherwise, implement it in your `post()` method.

5.  After implementing both methods, add your module's name in the `__all__` attribute in [tekinbot/comms/message/\_\_init\_\_.py](https://github.com/nanflasted/TekinBot/blob/documentation-branch/tekinbot/comms/message/__init__.py). Note that you can have sub-submodules (and should do so if your function consists of reactions to multiple different regexes) as long as you name them correctly (like `searching.youtube`).

6.  Write unit tests for your module: Tekin uses `pytest` to test all modules, should be pretty easy to pick up with examples from tests/comms/message/...; you should generally test your regex with a few test cases, test your process method to see if all the things you want are called correctly (remember to [`mock`](https://docs.python.org/3/library/unittest.mock.html) things out for non-flaky testing)

7.  If you'd like to manually test to see if it works, run a `python` shell and import your module from the base tekin directory, and call your `process()` method with a fake request object, usually you need something like:
    ```{json}
    {'event':{'text':'some texts to test your regex', 'user':'encrypted_user_id', 'ts':timestamp}}
    ```

    If your change concerns a database table, make sure you supply your database credentials as described in the main README doc, and change it back after you test so you don't commit it along with the changes. (I will make dev environment config separations in makefiles soon™ I promise). See the main README.md doc for more on how to database.

8.  If you'd like to test it in the real slack workspace, let me know! I can pull your branch locally and start a testing instance (I will try to make canaries soon™ I promise).

9.  Git commit, git push origin your-branch, make a pull request, and you are done! If you want to, go right ahead and merge your branch into master yourself (if you are sure of what you are doing); just make sure to let @nanflasted know that happened, so he actually pulls and deploys the changes (I will make automated deployment flow soon™ I promise).
