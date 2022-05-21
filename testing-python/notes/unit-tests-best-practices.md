# Tips for writing great unit tests

*  **Make each test orthogonal to (i.e., independent from) all the others**

   Any given behaviour should be specified in one *and only one* test. Otherwise if you later change that behaviour, you'll have to change multiple tests. The corollaries of this rule include:

  * Don't make unnecessary assertions

    Which specific behaviour are you testing? It's counterproductive to Assert() anything that's also asserted by another test: it just increases the frequency of pointless failures without improving unit test coverage one bit. This also applies to unnecessary Verify() calls -- if it isn't the core behaviour under test, then stop making observations about it! Sometimes, TDD folks express this by saying "*have only one logical assertion per test*". Remember, unit tests are a design specification of how a certain behaviour should work, not a list of observations of *everything* the code happens to do.

  * Test only one code unit at a time

    Your architecture *must* support testing units (i.e., classes or very small groups of classes) independently, not all chained together. Otherwise, you have lots of overlap between tests, so changes to one unit can cascade outwards and cause failures everywhere. If you can't do this, then your architecture is limiting your work's quality -- consider using Inversion of Control.

*   **Mock out all external services and state**

    Otherwise, behaviour in those external services overlaps multiple tests, and state data means that different unit tests can influence each other's outcome. You've definitely taken a wrong turn if you have to run your tests in a specific order, or if they only work when your database or network connection is active. (By the way, sometimes your architecture might mean your code touches static variables during unit tests. Avoid this if you can, but if you can't, at least make sure each test resets the relevant statics to a known state before it runs.)

*   **Avoid unnecessary preconditions**

    Avoid having common setup code that runs at the beginning of lots of unrelated tests. Otherwise, it's unclear what assumptions each test relies on, and indicates that you're not testing just a single unit. An exception: Sometimes I find it useful to have a common setup method shared by a *very* *small* number of unit tests (a handful at the most) but only if *all* those tests require *all* of those preconditions. This is related to the *context-specification* unit testing pattern, but still risks getting unmaintainable if you try to reuse the same setup code for a wide range of tests. (By the way, I wouldn't count pushing multiple data points through the same test (e.g., using NUnit's \[TestCase\] API) as violating this orthogonality rule. The test runner may display multiple failures if something changes, but it's still only one test method to maintain, so that's fine.)

*   **Don't unit-test configuration settings**

    By definition, your configuration settings aren't part of any unit of code (that's why you extracted the setting out of your unit's code). Even if you could write a unit test that inspects your configuration, it merely forces you to specify the same configuration in an additional redundant location. Congratulations: it proves that you can copy and paste! Personally I regard the use of things like filters in ASP.NET MVC as being configuration. Filters like \[Authorize\] or \[RequiresSsl\] are configuration options baked into the code. By all means write an integration test for the externally-observable behaviour, but it's meaningless to try unit testing for the filter attribute's presence in your source code -- it just proves that you can copy and paste again. That doesn't help you to design anything, and it won't ever detect any defects.

*   **Name your unit tests clearly and consistently**

    If you're testing how ProductController's Purchase action behaves when stock is zero, then maybe have a test fixture class called PurchasingTests with a unit test called ProductPurchaseAction\_IfStockIsZero\_RendersOutOfStockView(). This name describes the **subject** (ProductController's Purchase action), the **scenario** (stock is zero), and the **result** (renders "out of stock" view). I don't know whether there's an existing name for this naming pattern, though I know others follow it. How about **S/S/R**? Avoid non-descriptive unit tests names such as Purchase() or OutOfStock(). Maintenance is hard if you don't know what you're trying to maintain.


## Conclusion

Without doubt, unit testing *can* significantly increase the quality of your project. Many in our industry claim that [any unit tests are better than none](http://www.google.co.uk/search?q=any+unit+testing+is+better+than+none), but I disagree: a test suite can be a great asset, or it can be a great burden that contributes little. It depends on the quality of those tests, which seems to be determined by how well its developers have understood the goals and principles of unit testing.
