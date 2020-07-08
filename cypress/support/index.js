// Custom Commands
// https://docs.cypress.io/api/cypress-api/custom-commands.html

Cypress.Commands.add("flushDatabaseAndLoadFixtures", (fixtures) => {
  cy.exec(
    Cypress.env("DJANGO_MANAGE_COMMAND") +
      " flush-and-loaddata --no-input " +
      fixtures.join(" ")
  );
});

Cypress.Commands.add("loadFixture", (fixture) => {
  cy.exec(Cypress.env("DJANGO_MANAGE_COMMAND") + " loaddata " + fixture);
});

Cypress.Commands.add("doDraw", () => {
  cy.exec(
    Cypress.env("DJANGO_MANAGE_COMMAND") + " enqueue-scheduled-exchange-draws"
  );
});

Cypress.Commands.add("showMenu", (fixture) => {
  cy.get("nav section ul").invoke("show");
});

Cypress.Commands.add("visitUrlInEmail", () => {
  cy.request({
    url: "__lastemail__",
    retryOnStatusCodeFailure: true,
  }).then((response) => {
    const url = response.body.match(/(https?:[^\s]+)/)[0];
    return cy.visit(url);
  });
});
