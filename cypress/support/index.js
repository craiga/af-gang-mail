// Custom Commands
// https://docs.cypress.io/api/cypress-api/custom-commands.html

Cypress.Commands.add("resetAndLoadFixtures", (fixtures) => {
  cy.exec(
    Cypress.env("DJANGO_MANAGE_COMMAND") +
      " cypress-reset --no-input " +
      fixtures.join(" "),
    { env: { CYPRESS_BASE_URL: Cypress.config().baseUrl } }
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

Cypress.Commands.add("visitUrlInEmail", (messageSearch) => {
  const mailtrapHeaders = {
    "Api-Token": Cypress.env("MAILTRAP_API_TOKEN"),
  };
  const url =
    "https://mailtrap.io/api/v1/inboxes/" +
    Cypress.env("MAILTRAP_INBOX_ID") +
    "/messages?search=" +
    encodeURIComponent(messageSearch);
  cy.request({ url: url, headers: mailtrapHeaders })
    .its("body.0")
    .then((message) => {
      cy.request({
        url: "https://mailtrap.io" + message.txt_path,
        headers: mailtrapHeaders,
      }).then((response) => {
        const url = response.body.match(/(https?:[^\s]+)/)[0];
        return cy.visit(url);
      });
    });
});
