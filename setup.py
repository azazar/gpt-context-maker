from setuptools import setup, find_packages

setup(
    name="gpt-context-maker",
    version="0.2.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gpt-context-maker = gptcontextbuilder.main:main_cli',
        ],
    },
    install_requires=[
        'certifi==2023.5.7',
        'charset-normalizer==3.1.0',
        'flake8==6.0.0',
        'idna==3.4',
        'mccabe==0.7.0',
        'pathspec==0.11.1',
        'pycodestyle==2.10.0',
        'pyflakes==3.0.1',
        'pyperclip==1.8.2',
        'PyYAML==6.0',
        'regex==2023.6.3',
        'requests==2.31.0',
        'tiktoken==0.4.0',
        'urllib3==2.0.7',
    ],
)
