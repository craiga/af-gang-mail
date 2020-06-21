// Custom Commands
// https://docs.cypress.io/api/cypress-api/custom-commands.html

Cypress.Commands.add("flushDatabase", () => {
  cy.exec(Cypress.env("DJANGO_MANAGE_COMMAND") + " flush --no-input");
});

Cypress.Commands.add("loadFixture", (fixture) => {
  cy.exec(Cypress.env("DJANGO_MANAGE_COMMAND") + " loaddata " + fixture);
});
