# Code Quality

## Testing
Ensuring code functions as intended is a highly important part of the development process. There are 4 main levels of software testing:
* **Unit testing**: This involves testing the functionality of the smallest units of code that are reasonable to test. This is usually done at the function level, or can be done at the class level in an object orientated programming (OOP) environment. Each unit of code may be covered by multiple tests, depending on the cyclomatic complexity of the code. This ensures code with multiple branches or paths is fully tested. Often, these tests are written at the same time as the units of code they are testing. This allows the developer to verify the code works as intended when it was written, reducing the chances of bugs being added to the project. These tests can also be used to check for regressions when new code is being added or existing code is being refactored. Since all tests should be passing when new code is added, any failing tests are flags that previously working code has been broken. An example of a unit test would be checking the "add to cart" function of an online shop adds the correct item to the cart. There may need to be multiple variations of this test for different situations, including the cart being previously empty, the cart containing other items, the cart already containing that item etc.
* **Integration testing**: This involves checking the inter-operation of multiple subsystems. We have already verified each individual section works as intended with unit tests. This tries to verify if the components work together. An example of unit tests passing but integration tests failing would be if two subsystems expected different data formats for their communications. A similar issue to this caused the failure of the Mars Climate Orbiter space probe in 1999, when one system calculated a value in United States customary units (imperial) and the second system expected the value it received to be in SI units (metric) [18]. There is a wide spectrum of integration testing, from checking the interaction between two classes, to verifying the compatibility of two services in a service orientated architecture-based system.
* **System testing**: Also known as end-to-end testing, this involves testing the entire flow of a use case through the system. It is similar to an integration test in that it tests the interaction between subsystems, however it tests every part needed to fulfil the task rather than just a specific interaction. For an e-commerce website, this could be done by getting a bot to load the web page, sign in, search for an item, add it to the cart and then check out. They should aim to cover the main sequence of steps users are most likely to take.
* **Acceptance testing**: This is the only level of testing that can't entirely be automated, as it requires real users to interact with the system. It is the final round of checks that seek to determine whether the system is fit for purpose. Back when the waterfall software development model was common, this stage would likely involve giving the software to a team of quality assurance engineers (QA) for a period of time to try to discover bugs. Once they gave it the all-clear, it could be submitted to the product owner to get them to sign off on the system. Nowadays, with Agile methodologies being much more common and a much shorter average development lifecycle, it often involves deploying changes to a small group of users and relying on analytics and user feedback for results. For example, an online communication tool may rollout changes initially to internal employees to test out (known as "dogfooding"). Assuming the metrics indicate everything is ok, and no major bugs have been reported, they might proceed with a phased rollout. This means the updates are pushed to a small percentage of users first, and then incrementally released to all users over time. If any major issues are discovered, they are usually caught before they impact too many users and the faulty updates can be reverted.

The only type of testing I automated in this project was unit testing. I didn't automate the others because I felt they would take too much time for the little benefit they would return. The microservice based architecture allows changes to be isolated to a single subsystem, which reduced the functionality any single change could potentially impact. Also, as this is a single developer led project, mostly there was only one change in progress at a time. This allowed me to quickly manually test the new change and its small sphere of potential influence for bugs. For a larger project, these tests would be invaluable, however for this project they had too high a cost to benefit ratio to be prioritised ahead of other development work.

While I would have liked to implement automated unit testing covering all the services, the short time scale of the project limited what I could do. I evaluated the merits of implementing it on a service by service based and I felt there were only 2 services complex enough to justify automated testing: the classification service and the analyser service. All the other services mostly focus on data processing and transfer. They would be less likely to have buggy edge cases and any broken functionality would likely be picked up quickly by brief manual testing. Most of the complexity associated with the classifier service is to do with the generating of the model; the actual classification of tweets is actually quite simple. Given the generated machine learning model is tested first using cross validation, and then using a validation test set, I was satisfied this testing would be likely to catch any issues that were likely to occur. This left me to focus my unit testing efforts on the analyser service.

The analyser service generates analytics from large amounts of data, which would make it very difficult to notice small bugs in results. This is an ideal situation for unit testing to ensure results are what they are expected to be. The analyser service is made up of two separate Python modules, both of which I wanted to have as high a test coverage as is feasible.

The word cloud module doesn't connect to any external services which made it easier to test. It does rely on large amounts of data from the NLTK library however, which could break tests if the values get updated in the future. To counteract this, I mocked out the NLTK data with data I supplied, guaranteeing it won't break in the future. Unit tests should generally start with the simplest cases, and then get more complex if extra paths through the code aren't yet covered. An example unit test that covers the basics of the tweet parsing function is:
```` python
def test_parse_tweet_base_case(self):
    words = WordCloud.parse_tweet("alpha bravo charlie")
    self.assertEqual(["alpha", "bravo", "charlie"], words)
````
This covers the very basic functionality the function should provide, with only ASCII lower case characters and no punctuation. A more complex test to cover text with punctuation is:
```` python
def test_parse_tweet_with_punctuation(self):
    words = WordCloud.parse_tweet("alpha.. “bravo?” charlie’s delta! echo/2")
    self.assertEqual(["alpha", "bravo", "charlie's", "delta", "echo/2"], words)
````
A number of these test together cover all the various functionality of the tweet parsing function, ensuring it works as intended. As mentioned above, I needed to mock out the NLTK dataset to remove the dependency on the external system. A test where we do this is:
```` python
@mock.patch("wordcloud.webtext.raw")
def test_calculate_normal_word_freq(self, mocked_raw):
    mocked_raw.return_value = "man: Hello\n woman:HI\n man: hello again"

    normal_word_freq = wordcloud.calculate_normal_word_freq()
    self.assertEqual({"hello": 2, "hi": 1, "again": 1}, normal_word_freq)
````
The `@mock.patch` decorator replaces the NLTK webtext module's `raw` function with a `MagicMock` object. We can specify the value we want this mocked function to return when it is called. We then assert the word frequency the tested function calculates is equal to what we expected it to be, based on the mock data we specified.

The analyser module connects to both the database and the cache when it is started up, making it slightly harder to test. We can mock these out the same way we mocked the NLTK library, but it does increase the amount of boiler plate code needed in the tests. The analyser module being the "driver" code of the analyser service adds to the complexity of testing as it mostly deals with side effects (database reads, cache writes etc.) unlike the word cloud module. An example of a complex unit test verifying its driver functionality is:
````python
@mock.patch("analyser.Analyser.connect_to_db")
@mock.patch("analyser.Analyser.get_daily_avg_sentiment_by_viewpoint")
@mock.patch("analyser.Analyser.prune_old_tweets")
@mock.patch("analyser.Analyser.generate_word_clouds")
@mock.patch("analyser.time.sleep")
def test_run_infinitely(self, mocked_sleep, mocked_gen_wc, mocked_prune,
                        mocked_daily_senti, mocked_connect, mocked_redis):

    # Custom class used to stop the infinite loop
    class CustomExhausted(Exception):
        pass

    mocked_connect.return_value = (None, None)
    mocked_sleep.side_effect = [None, None, CustomExhausted]

    self.assertRaises(CustomExhausted, Analyser().run_infinitely)

    self.assertEqual(3, mocked_daily_senti.call_count)
    self.assertEqual(3, mocked_prune.call_count)
    self.assertEqual(3, mocked_gen_wc.call_count)
    self.assertEqual(3, mocked_sleep.call_count)
````
This complex test actually tests a far simpler function:
```` python
def run_infinitely(self, period=60):
    while True:
        self.get_daily_avg_sentiment_by_viewpoint()
        self.prune_old_tweets()
        self.generate_word_clouds()
        time.sleep(period)
````
The test is much longer and more complex than the function because it's quite a difficult function to test. To avoid re-testing the functions called inside the while loop, we're mocking them all out. This adds 3 extra mocks we have to handle, as well as the 2 mocks for the database and cache connections. Also, the code has an infinite loop causing it to run forever, but unit tests need to run and finish very quickly. A unit test that can't finish isn't of any use. To avoid this, we're mocking the `time.sleep` function to throw a special exception the 3rd time it is called. We're defining a custom exception for this to ensure it's raised because of our mock, rather than because of a hidden error in the code somewhere. We can then test that each of the functions inside the while loop are called 3 times as we expect, before we break the infinite loop.

Overall, the analyser has 99% line coverage from unit tests. It's not always feasible to push for 100%, as some code can't be or shouldn't be tested. The code that's not covered by the tests is:
```` python
if __name__ == '__main__':
    Analyser().run_infinitely()
````
This is python specific boiler plate that will execute the `run_infinitely` method if the module is being run directly, but not if the module is just being imported by some other module. Given the `run_infinitely` method is already covered by other tests, there is no need to try write a test to check this piece of code again. The results from the code coverage analysis are as follows:
````
.........................
----------------------------------------------------------------------
Ran 25 tests in 0.055s
OK
Name           Stmts   Miss  Cover   Missing
--------------------------------------------
analyser.py       68      1    99%   102
wordcloud.py      28      0   100%
--------------------------------------------
TOTAL             96      1    99%
````

## Linting
While testing checks how code runs, linting is the process of checking how code looks. Linters run static analysis against code to try find programming and stylistic errors. They don't execute code or test logic however. The languages I've set up linters for are Python, JavaScript and Dockerfiles.

Python linting is done using a Python module called flake8. This combines a number of Python style guidelines including PEP8 and Pyflakes into a single check. It warns about multiple issues including incorrect whitespace, unused variables, incorrect syntax and overly complex code. It can be configured using a `.flake8` config file at the root of the project structure. To keep every python based microservice consistent, I'm enforcing the same flake8 configuration across them all. I only have one custom override of the default style guide and that's increasing the maximum line length from 80 to 100 characters. This allows me to use slightly longer but more descriptive naming for variables and functions which I feel improves readability and clarity. To run the linter, run `flake8 .` from the root of the project structure.

JavaScript linting is done using ESLint. There are many JavaScript linters available but ESLint is one of the most customisable and flexible. It does need an initial configuration to get started however, as it isn't supplied with one like flake8. As a base ruleset, I chose the "Airbnb JavaScript Style Guide". It is one of the most popular style guides and it matches many of my preferences. I did override some of the style rules as I encountered situations where I disagreed with the base ruleset's defaults. My custom ESLint configuration is:
````YAML
{
    "extends": "airbnb-base",
    "parserOptions": {
        "sourceType": "script"
    },
    "rules": {
        "indent": ["error", 4],
        "no-console": "off",
        "no-restricted-syntax": [
            "error",
            "ForInStatement",
            "LabeledStatement",
            "WithStatement"
            // Removes For..Of from naughty list
        ],
        "no-plusplus": "off"
    }
}
````
The adjustments I've made can be seen above, which include setting the default indent width to 4 characters as well as removing the ban on console logging, the for..of loop and the unary increment operator (i.e. `i++`).

Dockerfile linting is done using Hadolint. It can validate inline bash commands as well as enforcing best practice for Docker image building. I didn't change any of the default configuration for this linter as it all felt correct to me. The hadolint program can be run without installation as it is distributed as a Docker image. Simply pull the image and then pipe the Dockerfile that needs to be tested into the running container. As Hadolint only supports linting a single Dockerfile at a time, I wrote a short bash script that finds all the Dockerfiles in the codebase and pipes them into it one by one.
```` bash
for filename in **/*.Dockerfile;
    do docker run --rm -i hadolint/hadolint < $filename;
done;
````
This allows the linter to validate every Dockerfile without needing to maintain a hard-coded list of their paths.

## Continuous Integration
With the large amount of various code tests and checks described above, running them all manually after making a change would be an intensive process. If one was missed it would increase the chances of bugs being added to the codebase. To automate away all of this, I've added in support for a continuous integration build and test service called Travis CI.

Continuous integration (CI) is the practice of merging code changes to the main version very frequently. This helps avoid the days of "integration hell" in other development methodologies where long periods of changes from many developers are all combined in the build up to a release. CI works well with agile development methodologies which focus on small, frequent changes. Every time a task is completed, there should be working code that can be merged to the main repository. These small changes should be easy to combine with the master copy as they are a small amount of work and shouldn't be too much out of date with the main branch.

A continuous integration service like Travis CI builds and tests every change before it can be merged to the master copy. This should ensure only good code is added. It is necessary as manual testing of every merge would be infeasible and error prone due to the frequency of merges in CI. Travis CI can be configured using a `.travis.yml` config file in the root of the repository. This is a YAML file that declares the checks that should be run to validate any change. I have it configured to run the analyser service's unit tests inside the analyser docker container (to match the production environment), to lint the Python code using flake8, the JavaScript code using ESLint and the Dockefiles using Hadolint. If any of these tests fail, or the unit test coverage for the analyser service drops below 95%, the build fails and the change is blocked.

Travis CI is one of many continuous integration services that all offer similar features. I've worked with others including Jenkins and Shippable in the past so I'm familiar with the alternatives. To choose a service for this project, I prepared a list of the features I would like it to have. These included automated test running, Docker support, cloud hosting and GitHub integration. As this project is mainly a learning experience, I ruled out Jenkins as it is the service I was most familiar with before starting. I was left with 3 competing options: Travis CI, Circle CI and Shippable. To choose between them in the end, I decided I should base it off popularity; the most popular service is probably also the one that's most valuable to know. It also leverages the "wisdom of the crowd", such that if a lot of other projects are using it, it's probably a good option to go with. To estimate service popularity, I ran a search on GitHub for any repositories that had files matching the naming scheme of the configuration file for each service. The results were as follows:

* Travis CI: [~32,000,000 results](https://github.com/search?utf8=%E2%9C%93&q=filename%3Atravis.yml&type=Code) for public GitHub repositories containing a `.travis.yml` file.
* Circle CI: [~121,000 results](https://github.com/search?utf8=%E2%9C%93&q=filename%3A.circle.yml&type=Code) for public GitHub repositories containing a `.circle.yml` file.
* Shippable: [~5,000 results](https://github.com/search?utf8=%E2%9C%93&q=filename%3Ashippable.yml&type=Code) for public GitHub repositories containing a `shippable.yml` file.

From these results, Travis CI was a clear winner. I'm aware this was far from a scientific test to calculate popularity, but it does give a rough figure which was enough for me to go on. All 3 services support similar features and have a similar YAML based configuration system so switching between them wouldn't be much hassle if it was needed at any stage.

To take full advantage of Travis, I've integrated it with the GitHub git repository I'm using for version control. It connects to GitHub via webhooks and listens for activity. I've protected the master branch of the repository to prevent anyone committing code directly to it. All changes must be committed to another branch and then a pull request opened to make changes to the master branch. For every commit on every branch of the project, Travis triggers a build to ensure everything is ok. The results are then displayed directly in the GitHub web UI next to the commit. When a pull request is opened, Travis runs another build against the changes ensuring they're still not breaking any tests. Only once that test passes does GitHub enable the pull request to be merged to master.
