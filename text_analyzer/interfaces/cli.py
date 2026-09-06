import click
import json
from application.use_cases import analyze_text
from infrastructure.language_detector import detect_language
from infrastructure.syllable_counters import get_syllable_counter
from infrastructure.sentiment import analyze_sentiment_textblob

@click.command()
@click.option('--text', help='Text to analyze')
@click.option('--file', type=click.File('r'), help='Input file')
@click.option('--batch-file', type=click.File('r'), help='JSON file with list of texts')
@click.option('--output', type=click.File('w'), help='Output file (JSON)')
def main(text, file, batch_file, output):
  if file:
    text = file.read()
  if batch_file:
    import json
    texts = json.load(batch_file)
    # обработать пакет
    # ...
  if not text:
    raise click.UsageError('Either --text, --file, or --batch-file required.')
  lang = detect_language(text)
  counter = get_syllable_counter(lang)
  result = analyze_text(text, detect_language, counter, analyze_sentiment_textblob)
  out_json = json.dumps(result.to_dict(), indent=2)
  if output:
    output.write(out_json)
  else:
    click.echo(out_json)


if __name__ == '__main__':
  main()
