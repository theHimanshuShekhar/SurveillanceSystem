import { Component, OnInit } from '@angular/core';
import { ResultService } from 'src/app/services/result.service';

@Component({
  selector: 'app-detection',
  templateUrl: './detection.component.html',
  styleUrls: ['./detection.component.scss']
})
export class DetectionComponent implements OnInit {

  constructor(private detectionService: ResultService) { }

  ngOnInit() {
    this.detectionService.getResults().subscribe(data => {
      console.log(data);
    });
  }

}
