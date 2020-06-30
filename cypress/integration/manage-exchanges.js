describe("Manage exchanges", () => {
  before(() => {
    cy.flushDatabaseAndLoadFixtures(["cypress/exchanges", "cypress/users"]);
  }),
    it("Admin can manage exchanges", () => {
      cy.visit("/");
      cy.get("[data-cy=login]")
        .contains("E-mail")
        .click()
        .type("admin@afgang.co.uk");
      cy.get("[data-cy=login]")
        .contains("Password")
        .click()
        .type("Dirty, rotten filthy scum!");
      cy.get("[data-cy=login]").contains("Log In").click();

      // Navigate to manage exchange page.
      cy.contains("Manage Exchanges").click();

      // Assert that exchanges are listed.
      cy.contains("Christmas 2050");
      cy.contains("Christmas 1978");

      // Navigate to eexchange detail page.
      cy.contains("Christmas 2050").click();

      // Assert exchange details are listed.
      cy.contains("Alice McUserFace");

      // Delete exchange from detail page.
      cy.contains("Delete").click();
      cy.get("button").click(); // confirm delete
      cy.contains("Christmas 2050").should("not.exist");

      // Delete another exchange from list page.
      cy.contains("tr", "Christmas 1978").contains("Delete").click();
      cy.get("button").click();
      cy.contains("Christmas 1978").should("not.exist");
    });
});
