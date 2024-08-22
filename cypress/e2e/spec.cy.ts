describe('template spec', () => {
  it('passes', () => {
    cy.visit('http://localhost:3000');
    cy.get('a[class=navbar-brand]').should('have.text', 'portfolio');
  });
});
