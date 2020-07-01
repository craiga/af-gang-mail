describe("Sign up", () => {
  before(() => {
    cy.flushDatabaseAndLoadFixtures(["cypress/exchanges"]);
  }),
    it("You can sign up from the home page", () => {
      cy.visit("/");
      cy.get("[data-cy=signup]")
        .contains("E-mail")
        .click()
        .type("zane@afgang.co.uk");
      cy.get("[data-cy=signup]")
        .contains("Password")
        .click()
        .type("This snowflake's an avalanche");
      cy.get("[data-cy=signup]").contains("Get Started").click();

      cy.contains("Hello zane@afgang.co.uk!");
      cy.contains("First name").click().type("Zane");
      cy.contains("Last name").click().type("Xylophone");
      cy.get(".pac-target-input").click().type("Fucking 10");
      cy.contains("Fucking, Austria").click();
      cy.get('input[name="address_city"]').should("have.value", "Fucking");
      cy.contains("Austria");
      cy.contains("Save").click();

      cy.contains("Thanks Zane Xylophone!");
      cy.contains("Christmas 2050").click();
      cy.contains("Join the Selected Exchanges").click();

      cy.contains("Your Name & Address");
      cy.contains("10 Fucking");
      cy.contains("Fucking");
      cy.contains("Oberösterreich");
      cy.contains("5121");
      cy.contains("Austria");
      cy.contains("Your Upcoming Exchanges");
      cy.contains("Christmas 2050");
      cy.contains("Your Past Exchanges");
    });
});
