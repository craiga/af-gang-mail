describe("Sign up", () => {
  before(() => {
    cy.resetAndLoadFixtures(["cypress/exchanges"]);
  });
  it("You can sign up from the home page", () => {
    cy.visit("/");
    cy.get("[data-cy=signup]")
      .contains("Email")
      .click()
      .type("zane@afgang.co.uk");
    cy.get("[data-cy=signup]")
      .contains("Password")
      .click()
      .type("This snowflake's an avalanche");
    cy.contains("Yes, this site can store my data").click();
    cy.get("[data-cy=signup]").contains("Get Started").click();

    cy.contains("Hello zane@afgang.co.uk!");
    cy.contains("sign-up-step-one-intro");
    cy.contains("First name").click().type("Zane");
    cy.contains("Last name").click().type("Xylophone");
    cy.get(".pac-target-input").click().type("8 Coral Court Hoppers");
    cy.contains("Hoppers Crossing").click();
    cy.get('input[name="address_postcode"]').should("have.value", "3029");
    cy.contains("Austria");
    cy.contains("Save").click();

    cy.contains("Thanks Zane Xylophone!");
    cy.contains("sign-up-step-two-intro");
    cy.contains("Christmas 2050").click();
    cy.contains("Join the Selected Exchanges").click();

    cy.contains("Thanks Zane Xylophone!");

    cy.contains("home-unverified-email-address");

    cy.contains("home-name-and-address-intro");
    cy.contains("8 Coral Court");
    cy.contains("Hoppers Crossing");
    cy.contains("3029");
    cy.contains("Victoria");
    cy.contains("Australia");

    cy.contains("home-upcoming-exchanges-intro");
    cy.contains("Christmas 2050");

    cy.contains("home-user-exchanges-intro");
  });
});
