import json

import click
from application.use_cases import analyzeText
from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentimentTextblob
from infrastructure.syllable_counters import getSyllableCounter


@click.command()
@click.option('--text', help='Text to analyze')
@click.option('--file', type=click.File('r'), help='Input file')
@click.option('--batch-file', type=click.File('r'), help='JSON file with list of texts')
@click.option('--output', type=click.File('w'), help='Output file (JSON)')
def main(text, file, batch_file, output):
  if file:
    text = file.read()
  if batch_file:
    texts = json.load(batch_file)
    # обработать пакет
    # ...
  if not text:
    raise click.UsageError('Either --text, --file, or --batch-file required.')
  lang = detectLanguage(text)
  counter = getSyllableCounter(lang)
  result = analyzeText(text, detectLanguage, counter, analyzeSentimentTextblob)
  out_json = json.dumps(result.to_dict(), indent=2)
  if output:
    output.write(out_json)
  else:
    click.echo(out_json)


if __name__ == '__main__':
  main()
