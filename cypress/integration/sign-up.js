describe("Sign up", () => {
  before(() => {
    cy.flushDatabase();
  }),
    it("You can sign up from the home page", () => {
      cy.visit("/");
      cy.get("[data-cy=signup]")
        .contains("E-mail")
        .click()
        .type("alice@afgang.co.uk");
      cy.get("[data-cy=signup]")
        .contains("Password")
        .click()
        .type("This snowflake's an avalanche");
      cy.get("[data-cy=signup]").contains("Get Started").click();

      cy.contains("Hello alice@afgang.co.uk!");
      cy.contains(
        "We've sent an email to alice@afgang.co.uk to verify your account. Please click the link in that email!"
      );
    });
});
