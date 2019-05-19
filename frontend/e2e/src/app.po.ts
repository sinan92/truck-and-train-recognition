import { browser, by, element } from 'protractor';

export class AppPage {
  canvas = element(by.css('agm-map'));
  navigateTo() {
    return browser.get('/');
  }

  getIdLoc() {
    return element(by.css('.mat-row:nth-child(1) > .cdk-column-id')).getText();
  }


   clickCanvas = function (toRight, toBottom) {
    browser.actions()
      .mouseMove(this.canvas, {x: toRight, y: toBottom})
      .click()
      .perform();
  };



  fillInput() {
    element(by.css('#mat-input-0')).sendKeys('1');
  }

  clickToevoegen() {
    element(by.css('#addMarker')).click();
  }
}
