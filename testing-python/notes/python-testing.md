# Testing, for Python developers

How many of you write software?
How many of you do so for a living?
How many of you test your software?
- If you said no, you are lying.
- Test = check that the program does what we think it does.
  We all do this very often in some manual way

Since we all need to verify that our software works, how can we
do it so that it is:
- Cheap
- Enjoyable


Basic take away message: we write automated tests to save ourselves time (==money)


---

Tests as executable specifications

---

Property testing (hypothesis - same principle as Haskell QuickCheck)

The key idea of property based testing is that rather than writing a test that
tests just a single scenario, you write tests that describe a range of
scenarios and then let the computer explore the possibilities for you rather
than having to hand-write every one yourself.

"There’s a simple invariant which every piece of software should satisfy, and
which can be remarkably powerful as a way to uncover surprisingly deep bugs in
your software.

That invariant is simple: The software shouldn’t crash. Or sometimes, it should
only crash in defined ways."


----
reading material (me) - Vladimir Khorikov's blog

http://enterprisecraftsmanship.com/2016/06/01/unit-tests-value-proposition/

A valuable test is a test that:

Has a high chance of catching a regression bug.
Has a low chance of producing a false positive.
Provides fast feedback.



http://enterprisecraftsmanship.com/2016/06/09/styles-of-unit-testing/

- Functional style (blackbox) http://i1.wp.com/i.imgur.com/yl79pi7.jpg?resize=502%2C211
- State verification (whitebox) http://i2.wp.com/i.imgur.com/jf6zSIj.jpg?resize=463%2C186
- Collaboration verification (white/graybox) http://i1.wp.com/i.imgur.com/p1EmKHG.jpg?resize=455%2C224


> there is another style of unit testing: property-based testing,
> which you can view as the functional style on steroids

The functional style has the best protection against false positives. Among all
other parts of the SUT, its input and output tend to change less frequently
during refactorings

The second style of unit testing – state verification – is more prone to false
positives but is still good enough as long as we verify the SUT’s state via its
public API and don’t try to analyze its content via reflection.  It’s still
unlikely to produce false positives because the SUT’s public API tends to stay
in place in the face of refactoring or addition of new functionality

What about the third style – collaboration verification? This is where the
value of unit tests starts to degrade.  The collaborations the SUT goes through
in order to achieve its goal are not part of its public API (arguable???).
Therefore, binding unit tests to the SUT’s collaborations introduces coupling
between the tests and the SUT’s implementation details.

The problem with mocks and with the mockist approach in general is that they
aim at verifying collaborations and often do that in a way that ties unit tests
to the implementation details of the SUT.

The use of mocks is just a sign of a problem, of course, not the problem
itself. However, it’s a very strong sign as it almost always signalizes an
issue with your approach to unit testing. If you use mocks, you most likely
couple your unit tests to the SUT’s implementation details.

There are a few legitimate use cases for mocks, though, but not in the context of unit testing. They can be useful in integration testing when you want to substitute a volatile dependency you don’t control. Also, mocks as an instrument also can be quite beneficial if you use them to create stubs.


http://enterprisecraftsmanship.com/2016/06/15/pragmatic-unit-testing/

To get the most of your unit tests, you need to treat the system you are
testing in as black-box manner as possible. It will help you avoid coupling
tests to the SUT’s implementation details and urge you to find ways to verify
the observable state of the system instead.

In practice, viewing the SUT as a black-box means that when it comes to unit
testing the domain model, you should forgo verifying collaborations between
your domain objects altogether and switch to the first two styles of unit
testing instead

there’s a big difference between knowing the SUT’s public API and its
implementation details. Never unit test against the latter.

The shift from verifying collaborations inside your domain model to the first
two (functional and state) styles of unit testing is not as simple as it might
seem and often requires architectural changes.


Volatile dependencies are dependencies that work with the outside world, for
example, with the database or an external HTTP service. Stable dependencies, on
the other hand, are self-contained and don’t interact with any resources
outside the process in which the SUT is executed.

Make sure you separate the code which contains business logic from the code
that has volatile dependencies.


your code should either depend on the outside world, or represent business
logic, but never both
(http://enterprisecraftsmanship.com/2015/07/06/how-to-do-painless-tdd/)

That is why building an isolated and self-contained domain model is important.
The onion architecture with the domain model at the center of it is exactly
about that [image]

You need to change the way you work with stable dependencies as well. Never
substitute them in tests and try to always use real objects <[e.g. from
factories]>. Mocking stable dependencies just doesn’t make any sense because
both the mock and the original object have predictable behavior which doesn’t
change because of external factors.

The definition Kent Beck gave to Unit Test has nothing to do with the SUT being
tested in isolation. Instead, it’s about a test running in isolation from other
tests.  In other words, a unit test is a test which can be run in parallel with
other unit tests because it doesn’t interfere with them through any shared
resources such as the database or the file system.  In practice, it means that
you shouldn’t substitute your domain classes with test doubles.

extracting an interface out of a domain entity in order to “enable unit
testing” is a design smell


The second architectural change here is reducing the number of layers of
indirection [...]  use as flat class structure as possible. That would allow
you to eliminate cyclic dependencies and reduce the complexity of your code
base.

The domain classes here are isolated from the outside world and interact with the minimum amount of peers all of which are also domain classes. The overall coordination is handled by application services (aka controllers / view models).

http://i0.wp.com/i.imgur.com/Hy1Xe0q.png?zoom=2&resize=499%2C373

Summary

- Pragmatic unit testing is about choosing to invest in the most valuable unit
  tests only. For the domain model, that are tests that focus on output and state
  verification, not collaboration verification.
- Adhering to pragmatic unit testing often requires architectural changes.
- Separate the code that contains domain knowledge from the code that has volatile dependencies.
- Don’t substitute stable dependencies, don’t introduce interfaces for domain
  classes in order to “enable unit testing”.
- Reduce the number of layers in your architecture. Have a single Application
  Services layer which talks directly to domain classes.


http://enterprisecraftsmanship.com/2016/06/21/pragmatic-integration-testing/

Integration tests are tests that, unlike unit tests, work with some of the
volatile dependencies directly (usually with the database and the file system)
They can potentially interfere with each other through those dependencies and
thus cannot run in parallel.

The coordination logic which resides in application services is left uncovered
by such tests <[unit tests as described above]>. While that’s certainly an
issue, a proper solution for it would be using integration tests, not unit
tests with mocks. ... What you can do instead is you can cover application
services with integration tests that will touch some of the volatile
dependencies. Such integration tests have a much better value proposition
because they do traverse a significant amount of real code and thus have a good
chance of catching a regression The downside here is that integration tests
achieve these benefits at the expense of being slow.


volatile dependencies themselves also fall into two categories: the ones you
can control (database and FS) and the ones you don’t have control overi (SMTP
service, message bus, 3rd party API.) - The latter is where mocks can actually
be helpful

How collaboration with those is different: When it comes to communicating with
the outside world, you have to preserve backward compatibility regardless of
the refactorings you perform (unlike when you refactor your own code) [1]. Here is
where collaboration verification testing can and should be used.

http://i2.wp.com/i.imgur.com/hZ9Debv.jpg?zoom=2&resize=494%2C415

[1] The way your domain objects communicate with each other is an
implementation detail whereas the way your application collaborates with other
applications is part of its public API.

Note that when working with volatile dependencies which you don’t have control
over, you need to always wrap them with your own gateways <(anti-corruption
layer?)>


A mock is a test double which allows you to verify that some method was invoked
during the test. It also lets you make sure this method is called using some
particular parameters. A stub, on the other hand, is a test double that just
returns some canned answer when you ask it. A spy is a test double that allows
you to record calls to some methods and examine them later on manually
(although, some authors also use the term “stub” for this kind of activity).

(You can use a mock-the-tool to introduce either a mock-the-test-double or a
stub)

This is essentially what differs a mock from a stub: mocks are used for
verifying side effects whereas stubs – for providing the SUT with test data.

In command-query separation, mocks are for commands; stubs are for queries.

Try to refrain from using mocks-the-test-doubles even when you need to
substitute a volatile dependency you application doesn’t control. Use spies
instead.

benefits of using a spy over a mock:
- you can set up the spy to gather only the information you need to verify, nothing more
- spies can be made reusable. And that allows you to gain additional protection against false positives


As integration tests is a much slower option comparing to unit tests, use them to cover the most important code paths only: happy paths and sophisticated edge cases.

Summary

- The communication pattern inside your domain model is an implementation
  detail; the way your application communicates with the outside world is part of
  its public API.
- Include volatile dependencies your application owns into your integration
  test suite; use test doubles to verify communications with the volatile
  dependencies you don’t have control over.
- There’s a difference between the concept of mock-the-tool and
  mock-the-test-double.
- Prefer using spies over mocks-the-test-doubles.


http://enterprisecraftsmanship.com/2015/07/13/integration-testing-or-how-to-sleep-well-at-nights/

The main difference between integration and unit testing is that integration tests actually affect external dependencies.

- Employ unit testing to verify all possible cases in your domain model.
- With integration tests, check only a single happy path per application service method. Also, if there are any edge cases which cannot be covered with unit tests, check them as well.



http://enterprisecraftsmanship.com/2016/07/05/growing-object-oriented-software-guided-by-tests-without-mocks/




http://blog.stevensanderson.com/2009/11/04/selective-unit-testing-costs-and-benefits/

the benefit of unit testing is correlated with the non-obviousness of the code under test.

In my experience, the remaining total cost of unit testing a certain code unit is very closely correlated with its number of dependencies on other code units.


http://blog.stevensanderson.com/2009/08/24/writing-great-unit-tests-best-and-worst-practises/


Goal 	Strongest technique
Finding bugs (things that don’t work as you want them to) 	Manual testing (sometimes also automated integration tests)
Detecting regressions (things that used to work but have unexpectedly stopped working) 	Automated integration tests (sometimes also manual testing, though time-consuming)
Designing software components robustly 	Unit testing (within the TDD process)

TDD is a robust way of designing software components (“units”) interactively so that their behaviour is specified through unit tests.

http://blog.stevensanderson.com/wp-content/uploads/2009/08/image-thumb1.png

<--- Unit tests contain a lot of knowledge about the behaviour of a single unit of code

---> integration tests contain no knowledge about how your codebase is broken down into units, but instead make statements about how the whole system behaves towards an external user

Anywhere in between, it’s unclear what assumptions you’re making and what you’re trying to prove.





----------------------

Arrange-Assert-Act

(http://enterprisecraftsmanship.com/2015/07/06/how-to-do-painless-tdd/):

- the fewer arrangements you do in a unit test, the more maintainable is becomes. In order to do this, you need to stop using mocks in your unit tests.

to make TDD painless. We need to unit test only a specific type of code which:

    Doesn’t have external dependencies.
    Expresses your domain.

Types of code:
https://lh3.googleusercontent.com/8SF2oeyuXO7xZmOzHPkxA1KnrDVuuY8FeONLNzpqSaA=w607-h572-no

 ---------+----------------
 domain   |   mess
 model    |
 ---------+----------------
 trivial  |  controllers,
          |  coordinators
 ---------+----------------

Generally, the maintainability cost of the code that both contains domain logic and has external dependencies (the “Mess” quadrant at the diagram) is too high

mess code should be split up: the domain logic should be placed in the domain objects so that the controller keeps track of coordination and putting it all together.

For best return of your investments, From the remaining 3 types of code in your code base (domain model, trivial code, and controllers), you need to unit test only the domain-related code:

- Not all code is equally important. Your application contains some business-critical parts (the domain model), on which you should focus the most of your efforts.
- Domain model is self-contained, it doesn’t depend on the external world. It means that you don’t need to use any mocks to test it, nor should you. Because of that, unit tests aimed to test your domain model are easy to implement and maintain.

The goal is to be confident that changes and new code don’t break existing functionality.

Summary:
- Don’t use mocks
- Extract the domain model out of methods with external dependencies
- Unit-test only the domain model
