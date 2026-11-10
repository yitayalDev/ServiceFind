import 'package:flutter_test/flutter_test.dart';
import 'package:service_finder/app/app.dart';

void main() {
  testWidgets('ServiceFinderApp builds without error', (WidgetTester tester) async {
    await tester.pumpWidget(const ServiceFinderApp());
    expect(find.text('ServiceFind'), findsOneWidget);
  });
}
