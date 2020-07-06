describe("Log in", () => {
  before(() => {
    cy.flushDatabaseAndLoadFixtures([
      "cypress/exchanges",
      "cypress/users",
      "cypress/draws",
    ]);
  }),
    it("User can log in and get details of active exchange.", () => {
      cy.visit("/");
      cy.get("[data-cy=login]")
        .contains("Email")
        .click()
        .type("alice@afgang.co.uk");
      cy.get("[data-cy=login]")
        .contains("Password")
        .click()
        .type("This snowflake's an avalanche");
      cy.get("[data-cy=login]").contains("Log In").click();

      cy.contains("Welcome back Alice McUserFace!");

      cy.contains("home-name-and-address-intro");
      cy.contains("340 Acton Mews");
      cy.contains("London");
      cy.contains("England");
      cy.contains("E8 4EA");
      cy.contains("United Kingdom");

      cy.contains("home-upcoming-exchanges-intro");

      cy.contains("home-past-exchanges-intro");

      cy.contains("You've been assigned Bob Userson in Cypress Test Exchange!");
    });
});
