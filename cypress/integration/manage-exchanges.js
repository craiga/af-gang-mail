describe("Manage exchanges", () => {
  before(() => {
    cy.flushDatabase();
    cy.loadFixture("cypress/manage-exchanges");
  }),
    it("User can delete exchange", () => {
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

      cy.contains("Manage Exchanges").click();
      cy.contains("Christmas 2050");
      cy.contains("Delete").click();
      cy.get("button").click();
      cy.contains("Christmas 2050").should("not.exist");
    });
});
