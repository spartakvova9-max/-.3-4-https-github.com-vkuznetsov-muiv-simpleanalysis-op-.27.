"""Render the supplied inspection table with larger text and stronger contrast.

Requires Pillow. Outputs lossless PNG, high-quality JPG, and a ZIP including BMP.
"""
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageDraw, ImageFont

FONT = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
ROWS = [
    ['Механизм', 'Проверка', 'Критерий приёмки'],
    ['Замок кейса (фиксатор крышки)', 'Закрыть / открыть',
     'Срабатывание с первого раза, отчётливая фиксация, без заедания'],
    ['Петли крышки', 'Открыть / закрыть',
     'Плавно, без скрипа и люфта; фиксация крышки в открытом положении'],
    ['Кнопки', 'Нажатие', 'Чёткий ход, самовозврат, без западания'],
    ['Переключатели', 'Переключение',
     'Фиксация в положениях, без самопроизвольного переключения'],
    ['Заглушки', 'Снять / установить',
     'Без заедания, с фиксацией; без повреждения'],
]


def main():
    font = ImageFont.truetype(str(FONT), 58)
    widths = [940, 740, 1420]
    padding, line_height, border = 32, 79, 6
    measure = ImageDraw.Draw(Image.new('RGB', (1, 1)))

    def wrap(text, width):
        lines = ['']
        for word in text.split():
            candidate = (lines[-1] + ' ' + word).strip()
            if measure.textlength(candidate, font=font) > width and lines[-1]:
                lines.append(word)
            else:
                lines[-1] = candidate
        return lines

    wrapped = [[wrap(text, width - 2 * padding) for text, width in zip(row, widths)]
               for row in ROWS]
    heights = [max(map(len, row)) * line_height + 2 * padding for row in wrapped]
    image = Image.new('RGB', (sum(widths) + border, sum(heights) + border), 'white')
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, image.width - 1, heights[0]), fill='#eeeeee')
    y = border // 2
    for row, height in zip(wrapped, heights):
        x = border // 2
        for lines, width in zip(row, widths):
            ty = y + (height - len(lines) * line_height) // 2
            for line in lines:
                draw.text((x + padding, ty), line, fill='black', font=font, anchor='lt')
                ty += line_height
            x += width
        y += height
    y = border // 2
    for height in heights:
        draw.line((0, y, image.width - 1, y), fill='black', width=border)
        y += height
    draw.line((0, y, image.width - 1, y), fill='black', width=border)
    x = border // 2
    for width in widths:
        draw.line((x, 0, x, image.height - 1), fill='black', width=border)
        x += width
    draw.line((x, 0, x, image.height - 1), fill='black', width=border)

    image.save('table_readable.png', dpi=(300, 300), optimize=True)
    image.save('table_readable.jpg', quality=100, subsampling=0, dpi=(300, 300))
    bmp = BytesIO()
    image.save(bmp, format='BMP')
    with ZipFile('table_readable_formats.zip', 'w', ZIP_DEFLATED) as archive:
        for name in ['table_readable.png', 'table_readable.jpg']:
            archive.write(name)
        archive.writestr('table_readable.bmp', bmp.getvalue())
        archive.writestr('README.txt',
            'Таблица перерисована с крупным жирным текстом и чёткими линиями.\n'
            'PNG и BMP сохраняют линии и текст без потерь. JPG дан для совместимости.\n'
            'Для вставки используйте PNG или BMP из этого архива.\n'
            'Не используйте скриншот предпросмотра. Передавайте архив как файл, не как фото.\n'
            'Если после вставки текст мелкий, увеличьте область таблицы в документе.\n'
            'При печати рекомендуется ширина таблицы не менее 18–20 см.\n')
    with ZipFile('table_readable_formats.zip') as archive:
        assert archive.testzip() is None
    print(f'Created {image.width} × {image.height} images and verified ZIP.')


if __name__ == '__main__':
    main()
