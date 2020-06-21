describe("Home Page", () => {
  before(() => {
    cy.flushDatabase();
  });
  it("Is accessible", () => {
    cy.visit("/");
    cy.contains("Hello, world");
  });
});
