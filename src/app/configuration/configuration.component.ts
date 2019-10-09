import { Component, OnInit } from '@angular/core';
import { ElectronService } from '../core/services';

@Component({
  selector: 'app-configuration',
  templateUrl: './configuration.component.html',
  styleUrls: ['./configuration.component.scss']
})

export class ConfigurationComponent implements OnInit {

  labels = [
    'person',
    'bicycle',
    'car',
    'motorbike',
    'aeroplane',
    'bus',
    'train',
    'truck',
    'boat',
    'traffic light',
    'fire hydrant',
    'stop sign',
    'parking meter',
    'bench',
    'bird',
    'cat',
    'dog',
    'horse',
    'sheep',
    'cow',
    'elephant',
    'bear',
    'zebra',
    'giraffe',
    'backpack',
    'umbrella',
    'handbag',
    'tie',
    'suitcase',
    'frisbee',
    'skis',
    'snowboard',
    'sports ball',
    'kite',
    'baseball bat',
    'baseball glove',
    'skateboard',
    'surfboard',
    'tennis racket',
    'bottle',
    'wine glass',
    'cup',
    'fork',
    'knife',
    'spoon',
    'bowl',
    'banana',
    'apple',
    'sandwich',
    'orange',
    'broccoli',
    'carrot',
    'hot dog',
    'pizza',
    'donut',
    'cake',
    'chair',
    'sofa',
    'pottedplant',
    'bed',
    'diningtable',
    'toilet',
    'tvmonitor',
    'laptop',
    'mouse',
    'remote',
    'keyboard',
    'cell phone',
    'microwave',
    'oven',
    'toaster',
    'sink',
    'refrigerator',
    'book',
    'clock',
    'vase',
    'scissors',
    'teddy bear',
    'hair drier',
    'toothbrush',
  ];

  selected = [];

  constructor(private electron: ElectronService) { }

  config;

  ngOnInit() {
    if (this.electron.fs.existsSync('config.json')) {
      const file = this.electron.fs.readFileSync('config.json', 'utf-8');
      this.config = JSON.parse(file);
      // @ts-ignore
      this.selected = this.config.selected_labels;
      console.log('config.json loaded');
      this.labels = this.labels.filter(label => this.selected.indexOf(label) < 0);
    } else {
      this.config = {};
    }
  }

  deselect(label) {
    this.labels.push(label);
    this.selected.splice(this.selected.indexOf(label), 1);
  }

  select(label) {
    this.selected.push(label);
    this.labels.splice(this.labels.indexOf(label), 1);
  }

  save() {
    this.config = { ...this.config, selected_labels: this.selected };
    this.electron.fs.writeFile('config.json', JSON.stringify(this.config), 'utf8', (err) => {
      if (err) {
        console.log('An error occured while writing JSON Object to File.');
        return console.log(err);
      }

      console.log('config.json file has been saved.');
    });
  }

}
