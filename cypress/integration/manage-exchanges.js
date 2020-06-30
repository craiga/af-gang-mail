describe("Manage exchanges", () => {
  before(() => {
    cy.flushDatabaseAndLoadFixtures(["cypress/exchanges", "cypress/users"]);
  }),
    beforeEach(() => {
      cy.loadFixture("cypress/exchanges");
    }),
    it("Admin can view exchange", () => {
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
      cy.contains("Christmas 2050").click();
      cy.contains("Alice McUserFace");
    });
  it("Admin can delete exchange from list ", () => {
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
  it("Admin can delete exchange from exchange detail", () => {
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

    cy.contains("Christmas 2050").click();

    cy.contains("Delete").click();

    cy.get("button").click();

    cy.contains("Christmas 2050").should("not.exist");
  });
});
