SHELL := sh
SCRIPT := src/spin/__init__.py

.PHONY: test install uninstall devinstall devuninstall format

test: # Syntax-check src/spin/__init__.py
	@PYTHONPYCACHEPREFIX= python -m py_compile $(SCRIPT) && echo "syntax: OK"

install: # Copy src/spin/__init__.py to ~/.local/lib/py/spin.py
	@mkdir -p $${HOME}/.local/lib/py
	install -m 0755 $(SCRIPT) $${HOME}/.local/lib/py/spin.py
	@echo "installed to $${HOME}/.local/lib/py/spin.py"

uninstall: # Remove the installed spin.py
	@rm -vf $${HOME}/.local/lib/py/spin.py

devinstall: # Symlink src/spin/__init__.py for live development
	@mkdir -p $${HOME}/.local/lib/py
	ln -s -f $$PWD/$(SCRIPT) $${HOME}/.local/lib/py/spin.py
	@echo "linked to $${HOME}/.local/lib/py/spin.py"

devuninstall: # Remove the development symlink
	@rm -vf $${HOME}/.local/lib/py/spin.py

format: # Format src/spin/__init__.py with black (if installed)
	@if command -v black >/dev/null 2>&1; then \
		black $(SCRIPT) && echo "black: OK"; \
	else \
		echo "black: not installed (skipped)"; \
	fi
