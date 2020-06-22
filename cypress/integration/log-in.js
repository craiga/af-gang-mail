describe("Log in", () => {
  before(() => {
    cy.flushDatabase();
    cy.loadFixture("cypress/user");
  }),
    it("You can log in from the home page", () => {
      cy.visit("/");
      cy.get("[data-cy=login]")
        .contains("E-mail")
        .click()
        .type("alice@afgang.co.uk");
      cy.get("[data-cy=login]")
        .contains("Password")
        .click()
        .type("This snowflake's an avalanche");
      cy.get("[data-cy=login]").contains("Log In").click();

      cy.contains("Welcome back Alice McUserFace!");
    });
});
