export const getPyodide = async (stdOutRedir, stdErrRedir, url) => {
	const pkgResponse = fetch('vpython.zip').then((x) => x.arrayBuffer());
	let pyodide;
	try {
		pyodide = await loadPyodide({
			indexURL: url,
			stdout: stdOutRedir ? stdOutRedir : null,
			stderr: stdErrRedir ? stdErrRedir : null
		});
	} catch (e) {
		console.log(e);
		throw e;
	}

	if (pyodide) {
		const pkgdata = await pkgResponse;
		console.log('Unpacking package');
		pyodide.unpackArchive(pkgdata, 'zip');
		console.log('Importing vpython package');
	}

	return pyodide;
};

export const setupGSCanvas = async () => {
	let display, scene;

	window.__context = {
		glowscript_container: $('#glowscript').removeAttr('id')
	};
	display = window.canvas;
	scene = display();
	return scene;
};
