describe("Active Exchange", () => {
  before(() => {
    cy.cleanEmail();
    cy.resetAndLoadFixtures(["cypress/exchanges", "cypress/users"]);
    cy.doDraw();
  });
  it("User can log in and get details of active exchange.", () => {
    cy.visit("/");
    cy.get("[data-cy=login]")
      .contains("Email")
      .click()
      .type("alice@afgang.co.uk");
    cy.get("[data-cy=login]")
      .contains("Password")
      .click()
      .type("This snowflake's an avalanche");
    cy.get("[data-cy=login]").contains("Log In").click();

    cy.contains("Welcome back Alice McUserFace!");

    cy.contains("home-name-and-address-intro");
    cy.contains("340 Acton Mews");
    cy.contains("London");
    cy.contains("England");
    cy.contains("E8 4EA");
    cy.contains("United Kingdom");

    cy.contains("home-upcoming-exchanges-intro");

    cy.contains("home-past-exchanges-intro");

    cy.contains("You've drawn Bob Userson in Cypress Test Exchange!");
    cy.contains("See More Details").click();

    cy.contains("draw-intro");
    cy.contains("You've drawn Bob Userson!");
    cy.contains("Bob Userson");
    cy.contains("74-76 Johnston Street");
    cy.contains("Fitzroy");
    cy.contains("Victoria");
    cy.contains("3065");
    cy.contains("Australia");
    cy.contains("Bob Userson has drawn you!");
  });
  it("User can get details of active exchange from email.", () => {
    cy.visitUrlInEmail("alice@afgang.co.uk");

    cy.contains("Email").click().type("alice@afgang.co.uk");
    cy.contains("Password").click().type("This snowflake's an avalanche");
    cy.contains("Log In").click();

    cy.contains("Welcome back Alice McUserFace!");

    cy.contains("draw-intro");
    cy.contains("Bob Userson");
    cy.contains("74-76 Johnston Street");
    cy.contains("Fitzroy");
    cy.contains("Victoria");
    cy.contains("3065");
    cy.contains("Australia");
  });
  it("User can mark their mail as sent.", () => {
    cy.visit("/");
    cy.get("[data-cy=login]")
      .contains("Email")
      .click()
      .type("alice@afgang.co.uk");
    cy.get("[data-cy=login]")
      .contains("Password")
      .click()
      .type("This snowflake's an avalanche");
    cy.get("[data-cy=login]").contains("Log In").click();

    cy.contains("You've drawn Bob Userson in Cypress Test Exchange!");
    cy.contains("See More Details").click();

    cy.contains("draw-intro");
    cy.contains("Mark as Sent").click();

    cy.contains("draw-sent-intro");
    cy.get("textarea").click().type("Test mail sent message");
    cy.contains("Send Confirmation").click();

    cy.contains("Thanks! We've let Bob Userson know that mail is on its way!");
    cy.contains("draw-intro");
    cy.contains("You sent your mail");

    cy.textInEmail("bob@afgang.co.uk", "Test mail sent message");
  });
  it("User can mark their mail as received.", () => {
    cy.visit("/");
    cy.get("[data-cy=login]")
      .contains("Email")
      .click()
      .type("alice@afgang.co.uk");
    cy.get("[data-cy=login]")
      .contains("Password")
      .click()
      .type("This snowflake's an avalanche");
    cy.get("[data-cy=login]").contains("Log In").click();

    cy.contains("You've drawn Bob Userson in Cypress Test Exchange!");
    cy.contains("See More Details").click();

    cy.contains("draw-intro");
    cy.contains("Bob Userson has drawn you!");
    cy.contains("Mark as Received").click();

    cy.contains("draw-received-intro");
    cy.get("textarea").click().type("Test mail received message");
    cy.contains("Send Confirmation").click();

    cy.contains(
      "Thanks! We've let Bob Userson know that you've received your mail!"
    );
    cy.contains("draw-intro");
    cy.contains("You received your mail");

    cy.textInEmail("bob@afgang.co.uk", "Test mail received message");
  });
});
