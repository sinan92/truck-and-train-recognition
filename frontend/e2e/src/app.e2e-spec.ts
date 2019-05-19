import { AppPage } from './app.po';
import {browser} from 'protractor';

describe('workspace-project App', () => {
  let page: AppPage;

  beforeEach(() => {
    page = new AppPage();
  });

  it('Should add a wagon', () => {
    page.navigateTo();
    browser.sleep(2000);
    page.clickCanvas(50, 50);
    browser.sleep(1000);
    page.fillInput();
    page.clickToevoegen();
    browser.sleep(1000);
    page.navigateTo();
    browser.sleep(2000);
    expect(page.getIdLoc()).toEqual('1');

  });
});
