import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddWizard } from './add-wizard';

describe('AddWizard', () => {
  let component: AddWizard;
  let fixture: ComponentFixture<AddWizard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddWizard],
    }).compileComponents();

    fixture = TestBed.createComponent(AddWizard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
