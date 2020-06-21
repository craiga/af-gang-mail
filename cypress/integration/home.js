describe("Home Page", () => {
  it("Accessible", () => {
    cy.visit("/");
    cy.contains("Hello, world");
  });
});
