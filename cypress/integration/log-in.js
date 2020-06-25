describe("Log in", () => {
  before(() => {
    cy.flushDatabase();
    cy.loadFixture("cypress/exchanges");
    cy.loadFixture("cypress/user");
  }),
    it("User can log in from the home page", () => {
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

      cy.contains("Your Name & Address");
      cy.contains("340 Acton Mews");
      cy.contains("London");
      cy.contains("England");
      cy.contains("E8 4EA");
      cy.contains("United Kingdom");
      cy.contains("Your Upcoming Exchanges");
      cy.contains("Your Past Exchanges");
    });
});
