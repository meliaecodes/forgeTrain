import { fetch } from '@forge/api';

export async function run(event, context) {
	console.log("event:");
	console.log(event);
	console.log(event.issue.fields.project);
	console.log(event.issue.fields.status);
	if(event.issue.fields.project.key == "LBT") {
		console.log("It's the Lego Build Team Project!");
		if(event.issue.fields.status.name == "Done") {
			console.log("do a victory lap!");
			await fetch("https://ca2e-159-196-169-219.ngrok-free.app/forward");

		}
		console.log('Toggle Lights!');
		await fetch("https://ca2e-159-196-169-219.ngrok-free.app/lights");
	}
}
