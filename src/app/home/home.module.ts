import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeRoutingModule } from './home-routing.module';

import { HomeComponent } from './home.component';
import { SharedModule } from '../shared/shared.module';
import { RecordingsComponent } from '../recordings/recordings.component';
import { ConfigurationComponent } from '../configuration/configuration.component';

@NgModule({
  declarations: [HomeComponent, RecordingsComponent, ConfigurationComponent],
  imports: [CommonModule, SharedModule, HomeRoutingModule]
})
export class HomeModule { }
