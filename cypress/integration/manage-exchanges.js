describe("Manage exchanges", () => {
  before(() => {
    cy.flushDatabase();
    cy.loadFixture("cypress/exchanges");
    cy.loadFixture("cypress/users");
  }),
    it("Admin can delete exchange", () => {
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

      cy.contains("Manage Exchanges").click();
      cy.contains("tr", "Christmas 2050").contains("Delete").click();
      cy.get("button").click();
      cy.contains("Christmas 2050").should("not.exist");
    });
});
