import { NgModule, Component } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LiveComponent } from './pages/live/live.component';
import { DetectionComponent } from './pages/detection/detection.component';
import { ConfigComponent } from './pages/config/config.component';
import { PlayerComponent } from './player/player.component';


const routes: Routes = [
  { path: 'live', component: LiveComponent },
  { path: 'detections', component: DetectionComponent },
  { path: 'configuration', component: ConfigComponent },
  { path: 'player/:path', component: PlayerComponent },
  { path: '**', redirectTo: '/detections' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
