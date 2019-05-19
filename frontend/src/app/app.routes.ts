import {Routes} from '@angular/router';
import {HomeComponent} from './home/home.component';
import {CamerasOverviewComponent} from './cameras-overview/cameras-overview.component';
import {SettingsComponent} from './settings/settings.component';
export const appRoutes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'overview', component: CamerasOverviewComponent },
  { path: 'settings', component: SettingsComponent },
  /*
  { path: 'home/:ordernumber', component: HomeComponent },
  { path: 'login', component: LoginComponent },*/
  { path: '', redirectTo: '/home', pathMatch: 'full' }
];
